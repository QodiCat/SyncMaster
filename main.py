import os
import json
import markdown
import requests
from typing import List, Dict
from abc import ABC, abstractmethod

class Platform(ABC):
    """平台基类,定义发布接口"""
    
    @abstractmethod
    def publish(self, title: str, content: str, tags: List[str] = None) -> bool:
        """发布内容到平台"""
        pass

    @abstractmethod
    def format_content(self, content: str) -> str:
        """针对平台格式化内容"""
        pass

class CSDN(Platform):
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.headers = {
            'Cookie': cookie,
            'Content-Type': 'application/json'
        }
        self.publish_url = 'https://blog-console-api.csdn.net/v1/article/publish'

    def format_content(self, content: str) -> str:
        # CSDN支持标准Markdown,不需要特殊处理
        return content

    def publish(self, title: str, content: str, tags: List[str] = None) -> bool:
        data = {
            'title': title,
            'content': self.format_content(content),
            'tag_names': tags or [],
            'categories': [],
            'channel': 3,  # 博客类型
            'type': 1,     # 原创
        }
        try:
            response = requests.post(
                self.publish_url,
                headers=self.headers,
                json=data
            )
            return response.status_code == 200
        except Exception as e:
            print(f'CSDN发布失败: {str(e)}')
            return False

if __name__ == '__main__':
    csdn=CSDN('cookie')