from ark.crypto.models.block import Block

# TODO: MOARD TESTS!!!

def test_serialize_full_correctly_serializes_block_and_its_transactions(dummy_block):
    expected = '0000000078d07901593a22002b324b8b33a85802070000007c5c3b0000000000801d2c040000000000c2eb0b00000000e00000003784b953afcf936bdffd43fdf005b5732b49c1fc6b11e195c364c20b2eb06282020f5df4d2bc736d12ce43af5b1663885a893fade7ee5e62b3cc59315a63e6a3253045022100eee6c37b5e592e99811d588532726353592923f347c701d52912e6d583443e400220277ffe38ad31e216ba0907c4738fed19b2071246b150c72c0a52bae4477ebe29ff000000fe00000000010000ff000000ff000000ff000000ff000000ff011e0062d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874f07a080000000000000000001e40fad23d21da7a4fd4decb5c49726ea22f5e6bf6304402204f12469157b19edd06ba25fcad3d4a5ef5b057c23f9e02de4641e6f8eef0553e022010121ab282f83efe1043de9c16bbf2c6845a03684229a0d7c965ffb9abdfb97830450221008327862f0b9178d6665f7d6674978c5caf749649558d814244b1c66cdf945c40022015918134ef01fed3fe2a2efde3327917731344332724522c75c2799a14f78717ff011e0060d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874e67a080000000000000000001e79c579fb08f448879c22fe965906b4e3b88d02ed304402205f82feb8c5d1d79c565c2ff7badb93e4c9827b132d135dda11cb25427d4ef8ac02205ff136f970533c4ec4c7d0cd1ea7e02d7b62629b66c6c93265f608d7f2389727304402207e912031fcc700d8a55fbc415993302a0d8e6aea128397141b640b6dba52331702201fd1ad3984e42af44f548907add6cb7ad72ca0070c8cc1d8dc9bbda208c56bd9ff011e0064d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874fa7a080000000000000000001e84fee45dde2b11525afe192a2e991d014ff93a36304502210083216e6969e068770e6d2fe5c244881002309df84d20290ddf3f858967ed010202202a479b3da5080ea475d310ff13494654b42db75886a8808bd211b4bdb9146a7a3045022100e1dcab3406bbeb968146a4a391909ce41df9b71592a753b001e7c2ee1d382c5102202a74aeafd4a152ec61854636fbae829c41f1416c1e0637a0809408394973099fff011e0061d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874e67a080000000000000000001e1d69583ede5ee82d220e74bffb36bae2ce762dfb3045022100cd4fa9855227be11e17201419dacfbbd5d9946df8d6792a9488160025693821402207fb83969bad6a26959f437b5bb88e255b0a48eb04964d0c0d29f7ee94bd15e11304402205f50c2991a17743d17ffbb09159cadc35a3f848044261842879ccf5be9d81c5e022023bf21c32fb6e94494104f15f8d3a942ab120d0abd6fb4c93790b68e1b307a79ff011e0062d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874f07a080000000000000000001e56f9a37a859f4f84e93ce7593e809b15a524db2930450221009c792062e13399ac6756b2e9f137194d06e106360ac0f3e24e55c7249cee0b3602205dc1d9c76d0451d1cb5a2396783a13e6d2d790ccfd49291e3d0a78349f7ea0e830440220083ba8a9af49b8be6e93794d71ec43ffc96a158375810e5d9f2478e71655315b0220278402ecaa1d224dab9f0f3b28295bbaea339c85c7400edafdc49df87439fc64ff011e0063d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874f07a080000000000000000001e0232a083c16aba4362dddec1b3050ffdd6d43f2e3044022063c65263e42be02bd9831b375c1d76a88332f00ed0557ecc1e7d2375ca40070902206797b5932c0bad68444beb5a38daa7cadf536ee2144e0d9777b812284d14374e3045022100b04da6692f75d43229ffd8486c1517e8952d38b4c03dfac38b6b360190a5c33e0220776622e5f09f92a1258b4a011f22181c977b622b8d1bbb2f83b42f4126d00739ff011e0060d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874e67a080000000000000000001eccc4fce0dc95f9951ee40c09a7ae807746cf51403045022100d4513c3608c2072e38e7a0e3bb8daf2cd5f7cc6fec9a5570dccd1eda696c591902202ecbbf3c9d0757be7b23c8b1cc6481c51600d158756c47fcb6f4a7f4893e31c4304402201fed4858d0806dd32220960900a871dd2f60e1f623af75feef9b1034a9a0a46402205a29b27c63fcc3e1ee1e77ecbbf4dd6e7db09901e7a09b9fd490cd68d62392cb'
    block = Block(dummy_block)
    serialized_full = block.serialize_full()
    assert serialized_full == expected


def test_serialize_correctly_serializes_just_the_block(dummy_block):
    expected = '0000000078d07901593a22002b324b8b33a85802070000007c5c3b0000000000801d2c040000000000c2eb0b00000000e00000003784b953afcf936bdffd43fdf005b5732b49c1fc6b11e195c364c20b2eb06282020f5df4d2bc736d12ce43af5b1663885a893fade7ee5e62b3cc59315a63e6a3253045022100eee6c37b5e592e99811d588532726353592923f347c701d52912e6d583443e400220277ffe38ad31e216ba0907c4738fed19b2071246b150c72c0a52bae4477ebe29'
    block = Block(dummy_block)
    serialized = block.serialize()
    assert serialized == expected


def test_creating_a_block_from_hex_header_only_correctly_sets_all_attributes():
    serialized = '0000000078d07901593a22002b324b8b33a85802070000007c5c3b0000000000801d2c040000000000c2eb0b00000000e00000003784b953afcf936bdffd43fdf005b5732b49c1fc6b11e195c364c20b2eb06282020f5df4d2bc736d12ce43af5b1663885a893fade7ee5e62b3cc59315a63e6a3253045022100eee6c37b5e592e99811d588532726353592923f347c701d52912e6d583443e400220277ffe38ad31e216ba0907c4738fed19b2071246b150c72c0a52bae4477ebe29'
    block = Block(serialized)
    assert block.version == 0
    assert block.timestamp == 24760440
    assert block.height == 2243161
    assert block.previous_block_hex == b'2b324b8b33a85802'
    assert block.previous_block == 3112633353705641986
    assert block.number_of_transactions == 7
    assert block.total_amount == 3890300
    assert block.total_fee == 70000000
    assert block.reward == 200000000
    assert block.payload_length == 224
    assert block.payload_hash == b'3784b953afcf936bdffd43fdf005b5732b49c1fc6b11e195c364c20b2eb06282'
    assert block.generator_public_key == b'020f5df4d2bc736d12ce43af5b1663885a893fade7ee5e62b3cc59315a63e6a325'
    assert block.block_signature == b'3045022100eee6c37b5e592e99811d588532726353592923f347c701d52912e6d583443e400220277ffe38ad31e216ba0907c4738fed19b2071246b150c72c0a52bae4477ebe29'
    assert block.id == 7176646138626297930
    assert block.id_hex == b'639891a3bb7fd04a'
    assert getattr(block, 'transactions', None) is None



def test_creating_a_block_from_hex_sets_all_attributes_including_transactions(dummy_block):
    serialized = '0000000078d07901593a22002b324b8b33a85802070000007c5c3b0000000000801d2c040000000000c2eb0b00000000e00000003784b953afcf936bdffd43fdf005b5732b49c1fc6b11e195c364c20b2eb06282020f5df4d2bc736d12ce43af5b1663885a893fade7ee5e62b3cc59315a63e6a3253045022100eee6c37b5e592e99811d588532726353592923f347c701d52912e6d583443e400220277ffe38ad31e216ba0907c4738fed19b2071246b150c72c0a52bae4477ebe29ff000000fe00000000010000ff000000ff000000ff000000ff000000ff011e0062d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874f07a080000000000000000001e40fad23d21da7a4fd4decb5c49726ea22f5e6bf6304402204f12469157b19edd06ba25fcad3d4a5ef5b057c23f9e02de4641e6f8eef0553e022010121ab282f83efe1043de9c16bbf2c6845a03684229a0d7c965ffb9abdfb97830450221008327862f0b9178d6665f7d6674978c5caf749649558d814244b1c66cdf945c40022015918134ef01fed3fe2a2efde3327917731344332724522c75c2799a14f78717ff011e0060d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874e67a080000000000000000001e79c579fb08f448879c22fe965906b4e3b88d02ed304402205f82feb8c5d1d79c565c2ff7badb93e4c9827b132d135dda11cb25427d4ef8ac02205ff136f970533c4ec4c7d0cd1ea7e02d7b62629b66c6c93265f608d7f2389727304402207e912031fcc700d8a55fbc415993302a0d8e6aea128397141b640b6dba52331702201fd1ad3984e42af44f548907add6cb7ad72ca0070c8cc1d8dc9bbda208c56bd9ff011e0064d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874fa7a080000000000000000001e84fee45dde2b11525afe192a2e991d014ff93a36304502210083216e6969e068770e6d2fe5c244881002309df84d20290ddf3f858967ed010202202a479b3da5080ea475d310ff13494654b42db75886a8808bd211b4bdb9146a7a3045022100e1dcab3406bbeb968146a4a391909ce41df9b71592a753b001e7c2ee1d382c5102202a74aeafd4a152ec61854636fbae829c41f1416c1e0637a0809408394973099fff011e0061d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874e67a080000000000000000001e1d69583ede5ee82d220e74bffb36bae2ce762dfb3045022100cd4fa9855227be11e17201419dacfbbd5d9946df8d6792a9488160025693821402207fb83969bad6a26959f437b5bb88e255b0a48eb04964d0c0d29f7ee94bd15e11304402205f50c2991a17743d17ffbb09159cadc35a3f848044261842879ccf5be9d81c5e022023bf21c32fb6e94494104f15f8d3a942ab120d0abd6fb4c93790b68e1b307a79ff011e0062d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874f07a080000000000000000001e56f9a37a859f4f84e93ce7593e809b15a524db2930450221009c792062e13399ac6756b2e9f137194d06e106360ac0f3e24e55c7249cee0b3602205dc1d9c76d0451d1cb5a2396783a13e6d2d790ccfd49291e3d0a78349f7ea0e830440220083ba8a9af49b8be6e93794d71ec43ffc96a158375810e5d9f2478e71655315b0220278402ecaa1d224dab9f0f3b28295bbaea339c85c7400edafdc49df87439fc64ff011e0063d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874f07a080000000000000000001e0232a083c16aba4362dddec1b3050ffdd6d43f2e3044022063c65263e42be02bd9831b375c1d76a88332f00ed0557ecc1e7d2375ca40070902206797b5932c0bad68444beb5a38daa7cadf536ee2144e0d9777b812284d14374e3045022100b04da6692f75d43229ffd8486c1517e8952d38b4c03dfac38b6b360190a5c33e0220776622e5f09f92a1258b4a011f22181c977b622b8d1bbb2f83b42f4126d00739ff011e0060d079010265c1f6b8c1966a90f3fed7bc32fd4f42238ab4938fdb2a4e7ddd01ae8b58b4c080969800000000001f476f6f736520566f746572202d205472756520426c6f636b20576569676874e67a080000000000000000001eccc4fce0dc95f9951ee40c09a7ae807746cf51403045022100d4513c3608c2072e38e7a0e3bb8daf2cd5f7cc6fec9a5570dccd1eda696c591902202ecbbf3c9d0757be7b23c8b1cc6481c51600d158756c47fcb6f4a7f4893e31c4304402201fed4858d0806dd32220960900a871dd2f60e1f623af75feef9b1034a9a0a46402205a29b27c63fcc3e1ee1e77ecbbf4dd6e7db09901e7a09b9fd490cd68d62392cb'
    block = Block(serialized)
    assert block.version == 0
    assert block.timestamp == 24760440
    assert block.height == 2243161
    assert block.previous_block_hex == b'2b324b8b33a85802'
    assert block.previous_block == 3112633353705641986
    assert block.number_of_transactions == 7
    assert block.total_amount == 3890300
    assert block.total_fee == 70000000
    assert block.reward == 200000000
    assert block.payload_length == 224
    assert block.payload_hash == b'3784b953afcf936bdffd43fdf005b5732b49c1fc6b11e195c364c20b2eb06282'
    assert block.generator_public_key == b'020f5df4d2bc736d12ce43af5b1663885a893fade7ee5e62b3cc59315a63e6a325'
    assert block.block_signature == b'3045022100eee6c37b5e592e99811d588532726353592923f347c701d52912e6d583443e400220277ffe38ad31e216ba0907c4738fed19b2071246b150c72c0a52bae4477ebe29'
    assert block.id == 7176646138626297930
    assert block.id_hex == b'639891a3bb7fd04a'
    assert len(block.transactions) == 7
    
    for transaction, expected in zip(block.transactions, dummy_block['transactions']):
        assert transaction.version == 1
        assert transaction.network == 30
        assert transaction.type == expected['type']
        assert transaction.timestamp == expected['timestamp']
        assert transaction.sender_public_key == expected['senderPublicKey'].encode('utf-8')
        assert transaction.fee == expected['fee']
        assert transaction.amount == expected['amount']
        assert transaction.asset == expected['asset']


def test_get_id_hex_returns_correct_hex(dummy_block):
    block = Block(dummy_block)
    assert block.get_id_hex() == b'639891a3bb7fd04a'


def test_get_id_returns_correct_id(dummy_block):
    block = Block(dummy_block)
    assert block.get_id() == 7176646138626297930
    