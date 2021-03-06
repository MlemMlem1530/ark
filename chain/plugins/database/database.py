import logging
import os
from collections import defaultdict
from hashlib import sha256

from playhouse.pool import PooledPostgresqlExtDatabase

from chain.crypto.objects.block import Block as CryptoBlock
from chain.crypto.objects.transactions import from_serialized
from chain.crypto.utils import calculate_round

from .models.block import Block
from .models.pool_transaction import PoolTransaction
from .models.round import Round
from .models.transaction import Transaction
from .wallet_manager import WalletManager

logger = logging.getLogger(__name__)


# TODO: inherit from interface
class Database(object):

    restored_database_integrity = False
    forging_delegates = []

    def __init__(self):
        super().__init__()
        self.db = PooledPostgresqlExtDatabase(
            database=os.environ.get("POSTGRES_DB_NAME", "postgres"),
            user=os.environ.get("POSTGRES_DB_USER", "postgres"),
            host=os.environ.get("POSTGRES_DB_HOST", "127.0.0.1"),
            port=os.environ.get("POSTGRES_DB_PORT", "5432"),
            # password='password'
            autorollback=True,
            max_connections=32,
            stale_timeout=300,  # 5 minutes
        )

        # TODO: figure this out (try with creating a base class and only assigning
        # _meta.database to that base class)
        Block._meta.database = self.db
        Transaction._meta.database = self.db
        Round._meta.database = self.db
        PoolTransaction._meta.database = self.db

        self._active_delegates = []

        self.wallets = WalletManager()

    def close(self):
        self.db.close()

    def get_last_block(self):
        """Get the last block
        Returns None if block can't be found.
        """
        try:
            block = Block.select().order_by(Block.height.desc()).get()
        except Block.DoesNotExist:
            return None
        else:
            crypto_block = CryptoBlock.from_object(block)
            return crypto_block

    def save_block(self, block):
        logger.info("Saving block %s", block.id)
        if not isinstance(block, CryptoBlock):
            raise Exception(
                "Block must be a type of crypto.objects.Block"
            )  # TODO: better exception

        with self.db.atomic() as db_txn:
            try:
                db_block = Block.from_crypto(block)
                db_block.save(force_insert=True)
            except Exception as e:  # TODO: Make this not so broad!
                logger.error("Got an exception while saving a block")
                db_txn.rollback()
                logger.error(e)
                return

        with self.db.atomic() as db_txn:
            try:
                for transaction in block.transactions:
                    db_transaction = Transaction.from_crypto(transaction)
                    db_transaction.save(force_insert=True)
            except Exception as e:  # TODO: Make this not so broad!
                logger.error("Got an exception while saving transactions")
                db_txn.rollback()
                db_block.delete_instance()
                logger.error(e)  # TODO: replace with logger.error
                raise e

    def apply_round(self, height):
        next_height = 1 if height == 1 else height + 1
        logger.info("Apply round next height: %s", next_height)
        current_round, _, max_delegates = calculate_round(next_height)
        logger.info("Current round %s", current_round)
        if next_height % max_delegates == 1:
            # TODO: Apparently forger can apply a round multiple times, so we need to
            # make sure that it only applies it once! Look at the code in ark core
            # to get the bigger picture of how it's done there
            logger.info("Starting round %s", current_round)

            # TODO: This is to update missed blocks on the wallet
            # self.update_delegate_stats(self.forging_delegates)
            # TODO: Save wallets to database
            # self.save_wallets

            # Get the active delegate list from in-memory wallet manager
            delegate_wallets = self.wallets.load_active_delegate_wallets(next_height)

            # TODO: ark core states that this is saving next round delegate list into
            # the db. Is that true? Or are we saving the current round delegate list
            # into the db?
            logger.info("STORING CURRENT ROUND %s", current_round)
            with self.db.atomic() as db_txn:
                try:
                    for wallet in delegate_wallets:
                        Round.create(
                            public_key=wallet.public_key,
                            balance=wallet.vote_balance,
                            round=current_round,
                        )
                except Exception as e:  # TODO: make this not so broad!
                    logger.error("Got an exception while saving a round")
                    db_txn.rollback()
                    logger.error(e)
                    raise e

    def apply_block(self, block):
        # TODO: implement this properly
        self.wallets.apply_block(block)

        # TODO: wat?
        # if (this.blocksInCurrentRound) {
        #     this.blocksInCurrentRound.push(block);
        # }
        self.save_block(block)
        self.apply_round(block.height)

        # TODO: em wat?
        # // Check if we recovered from a fork
        # if (state.forkedBlock &&
        #     state.forkedBlock.data.height === this.block.data.height) {
        #     this.logger.info("Successfully recovered from fork :star2:");
        #     state.forkedBlock = null;
        # }

    def verify_blockchain(self):
        """ Verify that the blockchain stored in the db is not corrupted

        This makes simple checks:
        - is last block available
        - is last block height equalt to the number of stored blocks
        - is the number of stored transactions equal to the number of sum of
        Block.number_of_transactions in the database
        - is the sum of all transaction fees equal to the sum of Block.total_fee
        - is the sum of all transaction amounts equal to the sum of Block.total_amount

        Returns a tuple (is_valid, errors)
        """
        errors = []

        last_block = self.get_last_block()

        block_stats = Block.statistics()
        transaction_stats = Transaction.statistics()

        if not last_block:
            errors.append("Last block is not available")
        else:
            if last_block.height != block_stats["blocks_count"]:
                errors.append(
                    "Last block height: {}, number of stored blocks: {}".format(
                        last_block.height, block_stats["blocks_count"]
                    )
                )

        # Number of stored transactions must be equal to the sum of
        # Block.number_of_transactions in the database
        if block_stats["transactions_count"] != transaction_stats["transactions_count"]:
            errors.append(
                (
                    "Number of transactions: {}, "
                    "number of transactions included in blocks: {}"
                ).format(
                    transaction_stats["transactions_count"],
                    block_stats["transactions_count"],
                )
            )

        # Sum of all transaction fees must equal to the sum of Block.total_fee
        if block_stats["total_fee"] != transaction_stats["total_fee"]:
            errors.append(
                (
                    "Total transaction fees: {}, "
                    "total transaction fees included in blocks: {}"
                ).format(transaction_stats["total_fee"], block_stats["total_fee"])
            )

        # Sum of all transaction amounts must equal to the sum of Block.total_amount
        if block_stats["total_amount"] != transaction_stats["total_amount"]:
            errors.append(
                (
                    "Total transaction amounts: {}, "
                    "total transaction amount included in blocks: {}"
                ).format(transaction_stats["total_amount"], block_stats["total_amount"])
            )

        is_valid = len(errors) == 0
        return is_valid, errors

    def get_active_delegates(self, height):
        """Get the top 51 delegates

        TODO: this function is potentially very broken and returns all rounds?
        """
        delegate_round, next_round, max_delegates = calculate_round(height)
        if not self._active_delegates or (
            self._active_delegates and self._active_delegates[0].round != delegate_round
        ):
            logger.info("Load delegates for round %s", delegate_round)
            delegates = list(
                Round.select()
                .where(Round.round == delegate_round)
                .order_by(Round.balance.desc(), Round.public_key.asc())
            )

            # for delegate in delegates:
            #     wallet = self.wallets.find_by_public_key(delegate.public_key)
            #     logger.info(
            #         "%s %s %s %s",
            #         delegate.public_key,
            #         delegate.balance,
            #         wallet.vote_balance,
            #         wallet.username,
            #     )

            if delegates:
                seed = sha256(str(delegate_round).encode("utf-8")).digest()
                # TODO: Look into why we don't reorder every 5th element
                # (the second index += 1
                # skips it). Also why do we create another seed, that is always the
                # same after the first run?
                # Apparently this order is used in forger. Might be better to put it
                # there instead of in a random function that doesn't tell you what it's
                # for, whatdoyouthink?
                index = 0
                while index < len(delegates):
                    for x in range(min(4, len(delegates) - index)):
                        new_index = seed[x] % len(delegates)
                        # Swap delegate on index with the delegate on new_index
                        delegates[new_index], delegates[index] = (
                            delegates[index],
                            delegates[new_index],
                        )
                        index += 1
                    seed = sha256(seed).digest()
                    index += 1

            self._active_delegates = delegates

        return self._active_delegates

    def get_recent_block_ids(self):
        """Get 10 most recent block ids
        """
        blocks = (
            Block.select(Block.id).order_by(Block.timestamp.desc()).limit(10).tuples()
        )
        return [x[0] for x in blocks]

    def get_block_by_id(self, block_id):
        try:
            block = Block.get(Block.id == block_id)
        except Block.DoesNotExist:
            return None
        else:
            return CryptoBlock.from_object(block)

    def get_forged_transaction_ids(self, transaction_ids):
        transactions = Transaction.select(Transaction.id).where(
            Transaction.id.in_(transaction_ids)
        )
        return [transaction.id for transaction in transactions]

    def transaction_is_forged(self, transaction_id):
        return Transaction.select().where(Transaction.id == transaction_id).exists()

    def get_blocks(self, height, limit, serialized, with_transactions=False):
        blocks = (
            Block.select()
            .where(Block.height.between(height, height + limit))
            .order_by(Block.height.asc())
        )

        if with_transactions:
            block_ids = [block.id for block in blocks]
            transactions = (
                Transaction.select()
                .where(Transaction.block_id.in_(block_ids))
                .order_by(Transaction.block_id.asc(), Transaction.sequence.asc())
            )

            transactions_map = defaultdict(list)
            for trans in transactions:
                # TODO: implement from_object on transaction and use that, instead of
                # creating it from serialized data.
                if serialized:
                    transactions_map[trans.block_id].append(trans.serialized)
                else:
                    transactions_map[trans.block_id].append(
                        from_serialized(trans.serialized)
                    )
        crypto_blocks = []
        for block in blocks:
            crypto_block = CryptoBlock.from_object(block)
            if with_transactions:
                crypto_block.transactions = transactions_map[block.id]
            crypto_blocks.append(crypto_block)
        return crypto_blocks

    def get_blocks_by_id(self, block_ids):
        blocks = (
            Block.select().where(Block.id.in_(block_ids)).order_by(Block.height.desc())
        )
        return [CryptoBlock.from_object(block) for block in blocks]

    def get_blocks_by_heights(self, heights):
        if not isinstance(heights, list):
            raise Exception("heights must be a type of list")

        blocks = Block.select().where(Block.height.in_(heights))
        return [CryptoBlock.from_object(block) for block in blocks]

    def delete_round(self, round_to_delete):
        Round.delete().where(Round.round == round_to_delete)

    def revert_block(self, block):
        current_round, next_round, max_delegates = calculate_round(block.height)
        if next_round == current_round + 1 and block.height > max_delegates:
            # const delegates = await this.calcPreviousActiveDelegates(round);
            # this.forgingDelegates = await this.getActiveDelegates(height, delegates);
            self.delete_round(next_round)

        self.wallets.revert_block(block)

    def rollback_to_round(self, to_round):
        # TODO: Get rid of this and use blockchain.revert_blocks instead
        """
        Removes all rounds, block and transactions to the start of the `to_round`.
        NOTE: You need to restart the chain after calling this as this does not rollback
        wallets and any data that's in memory/redis cache.
        """
        height = to_round * 51

        block_select_query = Block.select(Block.id).where(Block.height >= height)
        transaction_query = Transaction.delete().where(
            Transaction.block_id.in_(block_select_query)
        )
        deleted_transactions = transaction_query.execute()
        logger.info("Deleted transactions: %s", deleted_transactions)

        block_query = Block.delete().where(Block.height >= height)
        deleted_blocks = block_query.execute()
        logger.info("Deleted blocks: %s", deleted_blocks)

        round_query = Round.delete().where(Round.round > to_round)
        deleted_rounds = round_query.execute()
        logger.info("Deleted rounds: %s", deleted_rounds)
