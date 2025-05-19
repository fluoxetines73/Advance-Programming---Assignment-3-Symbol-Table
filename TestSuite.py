import unittest
from TestUtils import TestUtils


class TestSymbolTable(unittest.TestCase):
    # --------------------- INSERT ---------------------
    def test_1(self):
        inp = ["INSERT a number"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 1))

    def test_2(self):
        inp = ["INSERT a string"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 2))

    def test_3(self):
        inp = ["INSERT b2 number"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 3))

    def test_4(self):
        inp = ["INSERT b2 string"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 4))

    def test_5(self):
        inp = ["INSERT bE2 number"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 5))

    def test_6(self):
        inp = ["INSERT bE2 string"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 6))

    def test_7(self):
        inp = ["INSERT bE_2 number"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 7))

    def test_8(self):
        inp = ["INSERT b_ number"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 8))

    def test_9(self):
        inp = ["INSERT b_ string"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 9))

    def test_10(self):
        inp = ["INSERT b2_ number"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 10))

    def test_11(self):
        inp = ["INSERT b2_ string"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 11))

    def test_12(self):
        inp = ["INSERT string string"]
        exp = ["success"]
        self.assertTrue(TestUtils.check(inp, exp, 12))

    # --------------------- ASSIGN ---------------------
    def test_13(self):
        inp = ["INSERT x number", "ASSIGN x 1"]
        exp = ["success", "success"]
        self.assertTrue(TestUtils.check(inp, exp, 13))

    def test_14(self):
        inp = ["INSERT x number", "ASSIGN x 12.2"]
        exp = ["Invalid: ASSIGN x 12.2"]
        self.assertTrue(TestUtils.check(inp, exp, 14))

    def test_15(self):
        inp = ["INSERT x string", "ASSIGN x 'a'"]
        exp = ["success", "success"]
        self.assertTrue(TestUtils.check(inp, exp, 15))

    def test_16(self):
        inp = ["INSERT x number", "ASSIGN x 123"]
        exp = ["success", "success"]
        self.assertTrue(TestUtils.check(inp, exp, 16))

    def test_17(self):
        inp = ["INSERT x number", "ASSIGN x -122"]
        exp = ["Invalid: ASSIGN x -122"]
        self.assertTrue(TestUtils.check(inp, exp, 17))

    def test_18(self):
        inp = ["INSERT x string", "ASSIGN x '1'"]
        exp = ["success", "success"]
        self.assertTrue(TestUtils.check(inp, exp, 18))

    # --------------------- BEGIN+END ---------------------
    def test_19(self):
        inp = ["BEGIN", "END"]
        exp = []
        self.assertTrue(TestUtils.check(inp, exp, 19))

    def test_20(self):
        inp = ["INSERT x number", "BEGIN", "END x"]
        exp = ["Invalid: END x"]
        self.assertTrue(TestUtils.check(inp, exp, 20))

    def test_21(self):
        inp = ["INSERT x number", "BEGIN", "INSERT x number", "END"]
        exp = ["success", "success"]
        self.assertTrue(TestUtils.check(inp, exp, 21))

    def test_22(self):
        inp = ["INSERT x string", "BEGIN", "INSERT x string", "END"]
        exp = ["success", "success"]
        self.assertTrue(TestUtils.check(inp, exp, 22))

    def test_23(self):
        inp = ["BEGIN", "END", "END"]
        exp = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(inp, exp, 23))

    # --------------------- LOOKUP ---------------------
    def test_24(self):
        inp = ["LOOKUP B"]
        exp = ["Invalid: LOOKUP B"]
        self.assertTrue(TestUtils.check(inp, exp, 24))

    def test_25(self):
        inp = ["LOOKUP a"]
        exp = ["Undeclared: LOOKUP a"]
        self.assertTrue(TestUtils.check(inp, exp, 25))

    def test_26(self):
        inp = ["LOOKUP bE_2"]
        exp = ["Undeclared: LOOKUP bE_2"]
        self.assertTrue(TestUtils.check(inp, exp, 26))

    def test_27(self):
        inp = ["LOOKUP b_"]
        exp = ["Undeclared: LOOKUP b_"]
        self.assertTrue(TestUtils.check(inp, exp, 27))

    # --------------------- PRINT ---------------------
    def test_28(self):
        inp = ["PRINT"]
        exp = [""]
        self.assertTrue(TestUtils.check(inp, exp, 28))

    def test_29(self):
        inp = ["INSERT x number", "INSERT y number", "PRINT"]
        exp = ["success", "success", "x//0 y//0"]
        self.assertTrue(TestUtils.check(inp, exp, 29))

    # --------------------- RPRINT ---------------------
    def test_30(self):
        inp = ["RPRINT"]
        exp = [""]
        self.assertTrue(TestUtils.check(inp, exp, 30))

    def test_31(self):
        inp = [" RPRINT"]
        exp = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(inp, exp, 31))

    def test_32(self):
        inp = ["INSERT x number", "INSERT y number", "RPRINT"]
        exp = ["success", "success", "y//0 x//0"]
        self.assertTrue(TestUtils.check(inp, exp, 32))

    # --------------------- OTHER ---------------------
    def test_33(self):
        inp = [""]
        exp = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(inp, exp, 33))

    def test_34(self):
        inp = []
        exp = []
        self.assertTrue(TestUtils.check(inp, exp, 34))

    # --------------------- ASSIGN (tiếp) ---------------------
    def test_35(self):
        inp = ["INSERT x string", "ASSIGN x '1bc'"]
        exp = ["success", "success"]
        self.assertTrue(TestUtils.check(inp, exp, 35))

    # --------------------- BEGIN+END (tiếp) ---------------------
    def test_36(self):
        inp = ["BEGIN", "BEGIN", "END", "END", "END"]
        exp = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(inp, exp, 36))

    # --------------------- LOOKUP (tiếp) ---------------------
    def test_37(self):
        inp = ["LOOKUP string"]
        exp = ["Undeclared: LOOKUP string"]
        self.assertTrue(TestUtils.check(inp, exp, 37))

    # --------------------- PRINT (tiếp) ---------------------
    def test_38(self):
        inp = ["BEGIN", "INSERT x string", "INSERT y string", "PRINT", "END"]
        exp = ["success", "success", "x//1 y//1"]
        self.assertTrue(TestUtils.check(inp, exp, 38))

    # --------------------- RPRINT (tiếp) ---------------------
    def test_39(self):
        inp = ["BEGIN", "INSERT x string", "INSERT y string", "END", "RPRINT"]
        exp = ["success", "success", ""]
        self.assertTrue(TestUtils.check(inp, exp, 39))

    # --------------------- OTHER (tiếp) ---------------------
    def test_40(self):
        inp = ["INSERT x number", "number INSERT y number"]
        exp = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(inp, exp, 40))

    # --------------------- ASSIGN (tiếp) ---------------------
    def test_41(self):
        inp = ["INSERT x string", "ASSIGN x 'azAZ09'"]
        exp = ["success", "success"]
        self.assertTrue(TestUtils.check(inp, exp, 41))

    # --------------------- BEGIN+END (tiếp) ---------------------
    def test_42(self):
        inp = ["INSERT x string", "BEGIN", "INSERT x number", "ASSIGN x 1", "END"]
        exp = ["success", "success", "success"]
        self.assertTrue(TestUtils.check(inp, exp, 42))

    # --------------------- LOOKUP (tiếp) ---------------------
    def test_43(self):
        inp = ["LOOKUP x "]
        exp = ["Invalid: LOOKUP x "]
        self.assertTrue(TestUtils.check(inp, exp, 43))

    # --------------------- PRINT (tiếp) ---------------------
    def test_44(self):
        inp = ["INSERT x string", "INSERT y string", "BEGIN", "INSERT x string", "INSERT y string", "END", "PRINT"]
        exp = ["success", "success", "success", "success", "x//0 y//0"]
        self.assertTrue(TestUtils.check(inp, exp, 44))

    # --------------------- RPRINT (tiếp) ---------------------
    def test_45(self):
        inp = ["INSERT x string", "INSERT y string", "BEGIN", "INSERT x string", "RPRINT", "END"]
        exp = ["success", "success", "success", "x//1 y//0"]
        self.assertTrue(TestUtils.check(inp, exp, 45))

    # --------------------- OTHER (tiếp) ---------------------
    def test_46(self):
        inp = ["INSERT x number", " "]
        exp = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(inp, exp, 46))

    # --------------------- ASSIGN (tiếp) ---------------------
    def test_47(self):
        inp = ["INSERT x number", "ASSIGN x bc@ed"]
        exp = ["Invalid: ASSIGN x bc@ed"]
        self.assertTrue(TestUtils.check(inp, exp, 47))

    # --------------------- BEGIN+END (tiếp) ---------------------
    def test_48(self):
        inp = ["INSERT x number", "BEGIN", "INSERT x number", "END", "INSERT x number"]
        exp = ["Redeclared: INSERT x number"]
        self.assertTrue(TestUtils.check(inp, exp, 48))

    # --------------------- LOOKUP (tiếp) ---------------------
    def test_49(self):
        inp = ["INSERT x number", "LOOKUP x"]
        exp = ["success", "0"]
        self.assertTrue(TestUtils.check(inp, exp, 49))

    # --------------------- ASSIGN (tiếp) ---------------------
    def test_50(self):
        inp = ["INSERT x string", "ASSIGN x 1"]
        exp = ["TypeMismatch: ASSIGN x 1"]
        self.assertTrue(TestUtils.check(inp, exp, 50))

    def test_51(self):
        input = [
            "INSERT x string",
            "ASSIGN x '    '"
        ]
        
        expected = ["Invalid: ASSIGN x '    '"]
        self.assertTrue(TestUtils.check(input, expected, 51))

    def test_52(self):
        input = ["INSERT x number", "ASSIGN x b2"]
        expected = ["Undeclared: ASSIGN x b2"]

        self.assertTrue(TestUtils.check(input, expected, 52))

    def test_53(self):
        input = ["INSERT x number", "ASSIGN x 2b"]
        expected = ["Invalid: ASSIGN x 2b"]
        self.assertTrue(TestUtils.check(input, expected, 53))

