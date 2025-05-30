from PayLine import PayLine
from Role import PressOrder, Role, SymbolCombo, ValidSlip
from Symbol import Symbol

# redseven = Symbol(name='赤７', filename='redseven_1.png')
# print(redseven.id)
# print(redseven.name)
# print(redseven.filename)
# print(redseven.imagefile_path)
# print(redseven.image)

# upper_payline = PayLine(name='上段', paypos_L=0, paypos_C=0, paypos_R=0)
# print(upper_payline.id)
# print(upper_payline.name)
# print(upper_payline.paypos_L)
# print(upper_payline.paypos_C)
# print(upper_payline.paypos_R)
# print(upper_payline.payline)

vs_test_1 = ValidSlip(
    name="vs_test_1",
    validslip=([0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]),
)
print(vs_test_1.id, vs_test_1.name)
print(vs_test_1.validslip)

vs_test_2 = ValidSlip(
    name="vs_test_2",
    validslip=(0, [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]),
)
print(vs_test_2.id, vs_test_2.name)
print(vs_test_2.validslip)

vs_test_3 = ValidSlip(
    name="vs_test_3",
    validslip=(0, 0, 0),
)
print(vs_test_3.id, vs_test_3.name)
print(vs_test_3.validslip)

# vs_test_e1 = ValidSlip(
#     name="vs_test_e1",
#     validslip=([0, 1, 2, 3, 4], [0, 1, 2, 3, 4], 6),
# )
# print(vs_test_e1.id, vs_test_e1.name)
# print(vs_test_e1.validslip)

# vs_test_e2 = ValidSlip(
#     name="vs_test_e2",
#     validslip=([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]),
# )
# print(vs_test_e2.id, vs_test_e2.name)
# print(vs_test_e2.validslip)

# vs_test_e3 = ValidSlip(
#     name="vs_test_e3",
#     validslip=(
#         [0, 1, 2, 3, 4],
#         [0, 1, 2, 3, 4],
#         [0, 1, 2, 3, 4],
#         [0, 1, 2, 3, 4],
#     ),
# )
# print(vs_test_e3.id, vs_test_e3.name)
# print(vs_test_e3.validslip)

po_all = PressOrder(
    name="po_all",
    pressorder=([1, 2, 3], [1, 2, 3], [1, 2, 3]),
)
print(po_all.id, po_all.name)
print(po_all.pressorder)

po_123 = PressOrder(
    name="po_123",
    pressorder=(1, 2, 3),
)
print(po_123.id, po_123.name)
print(po_123.pressorder)

po_test_1 = PressOrder(
    name="po_test_1",
    pressorder=([2, 3], [1, 2, 3], [1, 2, 3]),
)
print(po_test_1.id, po_test_1.name)
print(po_test_1.pressorder)

# po_test_e1 = PressOrder(
#     name="po_test_e1",
#     pressorder=(4, [1, 2, 3], [1, 2, 3]),
# )
# print(po_test_e1.id, po_test_e1.name)
# print(po_test_e1.pressorder)

# po_test_e2 = PressOrder(
#     name="po_test_e2",
#     pressorder=([1, 2, 3, 4], [1, 2, 3], [1, 2, 3]),
# )
# print(po_test_e2.id, po_test_e2.name)
# print(po_test_e2.pressorder)

# po_test_e3 = PressOrder(
#     name="po_test_e3",
#     pressorder=([1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]),
# )
# print(po_test_e3.id, po_test_e3.name)
# print(po_test_e3.pressorder)

# 図柄
redseven = Symbol("赤７", "redseven_1.png")
blueseven = Symbol("青７", "blueseven_1.png")

# 有効ライン
PAYLINE_UPPER = PayLine("上段", payline=(0, 0, 0))
PAYLINE_MIDDLE = PayLine("中段", payline=(1, 1, 1))
PAYLINE_LOWER = PayLine("下段", payline=(2, 2, 2))
PAYLINE_RIGHTUP = PayLine("右上がり", payline=(2, 1, 0))
PAYLINE_RIGHTDOWN = PayLine("右下がり", payline=(0, 1, 2))

role_test_1 = Role(
    name="role_test_1",
    payout=15,
    symbolcombo=([redseven, blueseven], redseven, redseven),
    validpayline=[
        PAYLINE_UPPER,
        PAYLINE_MIDDLE,
        PAYLINE_LOWER,
        PAYLINE_RIGHTUP,
        PAYLINE_RIGHTDOWN,
    ],
    validslip=vs_test_1,
    pressorder=po_all,
)
print(role_test_1.id, role_test_1.name)
print(role_test_1.pressorder)
