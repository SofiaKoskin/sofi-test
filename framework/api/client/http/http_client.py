import json
import logging
from typing import Any
from urllib.parse import urljoin

import requests

from framework.settings import BASE_URL

# Настройка логирования для отладки
logger = logging.getLogger(__name__)


class APIError(Exception):
    """Кастомное исключение для ошибок API"""

    def __init__(self, status_code: int, response_text: str, url: str, method: str) -> None:
        self.status_code = status_code
        self.response_text = response_text
        self.url = url
        self.method = method
        super().__init__(f"API Error: {method} {url} -> {status_code}: {response_text}")


class APIClient:
    """
    Обертка над requests.
    """

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 30,
        headers: dict[str, str] | None = None,
        verify_ssl: bool = True,
    ) -> None:
        self.base_url = base_url or BASE_URL
        self.timeout = timeout
        self.headers = headers if headers else {}
        self.verify_ssl = verify_ssl

        # Для хранения cookies между запросами (если нужны)
        self.cookies: dict[str, str] = {}

    def _build_url(self, path: str) -> str:
        """Собирает полный URL"""
        return urljoin(self.base_url, path.lstrip("/"))

    def _log_request(self, method: str, url: str, **kwargs: Any) -> None:
        """Логирует запрос"""
        logger.info("=" * 120)
        logger.info(f"Request: {method} {url}")
        if request_json := kwargs.get("json"):
            logger.info(f"Request Body: {json.dumps(request_json, ensure_ascii=False)}")
        elif data := kwargs.get("data"):
            logger.info(f"Request Data: {data}")
        if params := kwargs.get("params"):
            logger.info(f"Request Params: {params}")
        if self.cookies:
            logger.info(f"Request Cookies: {self.cookies}")

    def _log_response(self, response: requests.Response) -> None:
        """Логирует ответ"""
        logger.info("=" * 120)
        logger.info(
            f"Response: status - {response.status_code}, method - {response.request.method} url - {response.url}"
        )
        if response.text and len(response.text) < 10000:
            logger.info(f"Response body: {response.text[:500]}")

    def _request(
        self,
        method: str,
        path: str,
        expected_status: int | None = None,
        raise_for_status: bool = True,
        **kwargs: Any,
    ) -> requests.Response:
        url = self._build_url(path=path)

        self._log_request(method=method, url=url, **kwargs)

        try:
            headers = self.headers.copy()

            if "headers" in kwargs:
                headers.update(kwargs.pop("headers"))

            if self.cookies:
                kwargs.setdefault("cookies", {}).update(self.cookies)

            response = requests.request(
                method=method,
                url=url,
                timeout=self.timeout,
                headers=headers,
                verify=self.verify_ssl,
                **kwargs,
            )

            if response.cookies:
                self.cookies.update(response.cookies.get_dict())

            self._log_response(response=response)

            if expected_status is not None and response.status_code != expected_status:
                raise APIError(
                    status_code=response.status_code,
                    response_text=response.text,
                    url=url,
                    method=method,
                )

            if raise_for_status and expected_status is None and response.status_code >= 400:
                raise APIError(
                    status_code=response.status_code,
                    response_text=response.text,
                    url=url,
                    method=method,
                )

            return response

        except requests.RequestException as e:
            logger.error(f"❌ Request failed: {e}")
            raise

    # ---------- Удобные методы для CRUD ----------

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        expected_status: int = 200,
        **kwargs: Any,
    ) -> requests.Response:
        """GET запрос"""
        return self._request(method="GET", path=path, params=params, expected_status=expected_status, **kwargs)

    def post(
        self,
        path: str,
        data: dict | None = None,
        json: dict | None = None,
        expected_status: int | None = 201,
        **kwargs: Any,
    ) -> requests.Response:
        """POST запрос"""
        return self._request(
            method="POST",
            path=path,
            data=data,
            json=json,
            expected_status=expected_status,
            **kwargs,
        )

    def put(
        self,
        path: str,
        data: dict | None = None,
        json: dict | None = None,
        expected_status: int | None = 200,
        **kwargs: Any,
    ) -> requests.Response:
        """PUT запрос"""
        return self._request(method="PUT", path=path, data=data, json=json, expected_status=expected_status, **kwargs)

    def patch(
        self,
        path: str,
        data: dict | None = None,
        json: dict | None = None,
        expected_status: int | None = 200,
        **kwargs: Any,
    ) -> requests.Response:
        """PATCH запрос"""
        return self._request(
            method="PATCH",
            path=path,
            data=data,
            json=json,
            expected_status=expected_status,
            **kwargs,
        )

    def delete(self, path: str, expected_status: int | None = 204, **kwargs: Any) -> requests.Response:
        """DELETE запрос"""
        return self._request(method="DELETE", path=path, expected_status=expected_status, **kwargs)

    # ---------- Утилиты ----------

    def set_auth_token(self, token: str):
        """Установить токен для авторизации"""
        self.headers["Authorization"] = f"Bearer {token}"

    def set_header(self, key: str, value: str):
        """Установить кастомный заголовок"""
        self.headers[key] = value

    def remove_header(self, key: str):
        """Удалить заголовок"""
        if key in self.headers:
            del self.headers[key]

    def set_cookie(self, key: str, value: str):
        """Установить cookie для последующих запросов"""
        self.cookies[key] = value

    def clear_cookies(self):
        """Очистить все cookies"""
        self.cookies.clear()

    def reset_headers(self):
        """Сбросить заголовки до дефолтных"""
        self.headers = {}

    def get_json(self, path: str, **kwargs: Any) -> Any:
        """GET запрос, возвращающий JSON (без проверки статуса)"""
        response = self.get(path=path, **kwargs)
        return response.json()

    def post_json(self, path: str, json: dict, **kwargs: Any) -> Any:
        """POST запрос, возвращающий JSON"""
        response = self.post(path=path, json=json, **kwargs)
        return response.json()

    def put_json(self, path: str, json: dict, **kwargs: Any) -> Any:
        """PUT запрос, возвращающий JSON"""
        response = self.put(path=path, json=json, **kwargs)
        return response.json()

    def patch_json(self, path: str, json: dict, **kwargs: Any) -> Any:
        """PATCH запрос, возвращающий JSON"""
        response = self.patch(path=path, json=json, **kwargs)
        return response.json()

    def delete_json(self, path: str, **kwargs: Any) -> Any:
        """DELETE запрос, возвращающий JSON"""
        response = self.delete(path=path, **kwargs)
        if response.status_code == 204:
            return {}
        return response.json()

    def copy(self) -> APIClient:
        """Создать копию клиента с теми же настройками"""
        new_client = APIClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers.copy(),
            verify_ssl=self.verify_ssl,
        )
        new_client.cookies = self.cookies.copy()
        return new_client
