import pytest
from unittest.mock import Mock
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from function_app import _text_response, _validate_param, multiply, divide
import azure.functions as func


class TestTextResponse:
    """_text_response関数のテスト"""
    
    def test_text_response_returns_correct_status(self):
        """正常なステータスコード200を返すことを確認"""
        response = _text_response("test message")
        assert response.status_code == 200
    
    def test_text_response_returns_correct_mimetype(self):
        """Content-Typeがtext/plainであることを確認"""
        response = _text_response("test message")
        assert response.mimetype == "text/plain"
    
    def test_text_response_returns_correct_message(self):
        """正しいメッセージを返すことを確認"""
        message = "test message"
        response = _text_response(message)
        assert response.get_body().decode() == message


class TestValidateParam:
    """_validate_param関数のテスト"""
    
    def test_valid_positive_integer(self):
        """正の整数が正しく処理されることを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.return_value = "123"
        value, err = _validate_param(req, "A")
        assert value == 123
        assert err is None
    
    def test_valid_zero(self):
        """0が正しく処理されることを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.return_value = "0"
        value, err = _validate_param(req, "A")
        assert value == 0
        assert err is None
    
    def test_missing_parameter(self):
        """パラメータが未指定の場合のエラーメッセージを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.return_value = None
        value, err = _validate_param(req, "A")
        assert value is None
        assert err == "Aが指定されていません"
    
    def test_invalid_string(self):
        """文字列が不正として処理されることを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.return_value = "abc"
        value, err = _validate_param(req, "B")
        assert value is None
        assert err == "Bが不正です"
    
    def test_negative_integer(self):
        """負の整数が不正として処理されることを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.return_value = "-1"
        value, err = _validate_param(req, "A")
        assert value is None
        assert err == "Aが不正です"
    
    def test_decimal_number(self):
        """小数点が不正として処理されることを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get.return_value = "1.5"
        value, err = _validate_param(req, "B")
        assert value is None
        assert err == "Bが不正です"


class TestMultiply:
    """multiply関数のテスト"""
    
    def test_multiply_valid_numbers(self):
        """正常な掛け算の結果を確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "2" if x == "A" else "3" if x == "B" else None
        response = multiply(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "6"
    
    def test_multiply_with_zero(self):
        """0との掛け算を確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "5" if x == "A" else "0" if x == "B" else None
        response = multiply(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "0"
    
    def test_multiply_large_numbers(self):
        """大きな数の掛け算を確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "100" if x == "A" else "200" if x == "B" else None
        response = multiply(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "20000"
    
    def test_multiply_missing_a(self):
        """Aが未指定の場合のエラーメッセージを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: None if x == "A" else "3" if x == "B" else None
        response = multiply(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "Aが指定されていません"
    
    def test_multiply_missing_b(self):
        """Bが未指定の場合のエラーメッセージを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "2" if x == "A" else None if x == "B" else None
        response = multiply(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "Bが指定されていません"
    
    def test_multiply_invalid_a(self):
        """Aが不正な場合のエラーメッセージを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "abc" if x == "A" else "3" if x == "B" else None
        response = multiply(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "Aが不正です"
    
    def test_multiply_invalid_b(self):
        """Bが不正な場合のエラーメッセージを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "2" if x == "A" else "-1" if x == "B" else None
        response = multiply(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "Bが不正です"


class TestDivide:
    """divide関数のテスト"""
    
    def test_divide_valid_numbers(self):
        """正常な割り算の結果を確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "6" if x == "A" else "3" if x == "B" else None
        response = divide(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "2"
    
    def test_divide_with_remainder(self):
        """小数点以下が切り捨てられることを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "1" if x == "A" else "2" if x == "B" else None
        response = divide(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "0"
    
    def test_divide_by_zero(self):
        """0除算のエラーメッセージを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "5" if x == "A" else "0" if x == "B" else None
        response = divide(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "Bは0にできません"
    
    def test_divide_zero_by_number(self):
        """0を割る場合の結果を確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "0" if x == "A" else "5" if x == "B" else None
        response = divide(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "0"
    
    def test_divide_missing_a(self):
        """Aが未指定の場合のエラーメッセージを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: None if x == "A" else "3" if x == "B" else None
        response = divide(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "Aが指定されていません"
    
    def test_divide_missing_b(self):
        """Bが未指定の場合のエラーメッセージを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "6" if x == "A" else None if x == "B" else None
        response = divide(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "Bが指定されていません"
    
    def test_divide_invalid_a(self):
        """Aが不正な場合のエラーメッセージを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "xyz" if x == "A" else "3" if x == "B" else None
        response = divide(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "Aが不正です"
    
    def test_divide_invalid_b(self):
        """Bが不正な場合のエラーメッセージを確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "6" if x == "A" else "-2" if x == "B" else None
        response = divide(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "Bが不正です"
    
    def test_divide_large_numbers(self):
        """大きな数の割り算を確認"""
        req = Mock(spec=func.HttpRequest)
        req.params.get = lambda x: "1000" if x == "A" else "7" if x == "B" else None
        response = divide(req)
        assert response.status_code == 200
        assert response.get_body().decode() == "142"
