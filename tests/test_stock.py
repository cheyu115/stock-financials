from app.stock import calculate_pe_ratio, calculate_peg_ratio


class TestCalculatePERatio:
    def test_pe_ratio_happy_path(self):
        """
        Happy Path: 正常合理的股價與 EPS，應該正確計算出四捨五入到小數點後兩位的 PE
        """
        assert calculate_pe_ratio(100.0, 5.0) == 20.0
        assert (
            calculate_pe_ratio(100.0, 3.0) == 33.33
        )  # 測試四捨五入 (100/3 = 33.333...)

    def test_pe_ratio_sad_path(self):
        """
        Sad Path: 公司虧損 (EPS 為負數)，此時本益比沒有意義，系統應防呆回傳 0.0
        """
        assert calculate_pe_ratio(100.0, -2.5) == 0.0

    def test_pe_ratio_edge_case(self):
        """
        Edge Case: EPS 剛好為 0，必須攔截 ZeroDivisionError 並回傳 0.0
        """
        assert calculate_pe_ratio(100.0, 0.0) == 0.0


class TestCalculatePEGRatio:
    def test_peg_ratio_happy_path(self):
        """
        Happy Path: 正常的本益比與預估成長率，正確計算 PEG
        """
        assert calculate_peg_ratio(20.0, 10.0) == 2.0
        assert calculate_peg_ratio(20.0, 3.0) == 6.67  # 測試四捨五入 (20/3 = 6.666...)

    def test_peg_ratio_sad_path(self):
        """
        Sad Path: 預估成長率為負數 (公司衰退)，PEG 在財務上不具意義，應回傳 0.0
        """
        assert calculate_peg_ratio(20.0, -5.0) == 0.0

    def test_peg_ratio_edge_case(self):
        """
        Edge Case: 成長率剛好為 0，必須攔截 ZeroDivisionError (除以零錯誤) 並回傳 0.0
        """
        assert calculate_peg_ratio(20.0, 0.0) == 0.0
