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

class Zhihu(Platform):
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.headers = {
            'Cookie': cookie,
            'Content-Type': 'application/json'
        }
        self.publish_url = 'https://api.zhihu.com/articles'

    def format_content(self, content: str) -> str:
        # 知乎文章使用HTML格式
        html = markdown.markdown(content)
        return html

    def publish(self, title: str, content: str, tags: List[str] = None) -> bool:
        data = {
            'title': title,
            'content': self.format_content(content),
            'topics': tags or [],
            'type': 'article'
        }
        try:
            response = requests.post(
                self.publish_url,
                headers=self.headers,
                json=data
            )
            return response.status_code == 200
        except Exception as e:
            print(f'知乎发布失败: {str(e)}')
            return False

class Twitter(Platform):
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str):
        import tweepy
        self.auth = tweepy.OAuthHandler(api_key, api_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

    def format_content(self, content: str) -> str:
        # Twitter字数限制,需要截断或分段
        return content[:280]

    def publish(self, title: str, content: str, tags: List[str] = None) -> bool:
        try:
            tweet_content = f"{title}\n\n{self.format_content(content)}"
            if tags:
                tweet_content += "\n" + " ".join([f"#{tag}" for tag in tags])
            
            self.api.update_status(tweet_content)
            return True
        except Exception as e:
            print(f'Twitter发布失败: {str(e)}')
            return False

class ContentSyncer:
    """内容同步管理器"""
    
    def __init__(self, platforms: Dict[str, Platform]):
        self.platforms = platforms

    def sync_publish(self, md_file: str, title: str = None, tags: List[str] = None):
        """同步发布Markdown文件到所有平台"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not title:
                # 从文件名或内容第一行提取标题
                title = os.path.splitext(os.path.basename(md_file))[0]
            
            results = {}
            for platform_name, platform in self.platforms.items():
                success = platform.publish(title, content, tags)
                results[platform_name] = success
                
            return results
            
        except Exception as e:
            print(f'同步发布失败: {str(e)}')
            return None

def load_config(config_file: str) -> Dict:
    """加载平台配置"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    # 加载配置
    config = load_config('config.json')
    
    # 初始化各平台
    platforms = {
        'csdn': CSDN(config['csdn']['cookie']),
        'zhihu': Zhihu(config['zhihu']['cookie']),
        'twitter': Twitter(
            config['twitter']['api_key'],
            config['twitter']['api_secret'],
            config['twitter']['access_token'],
            config['twitter']['access_token_secret']
        )
    }
    
    # 创建同步器
    syncer = ContentSyncer(platforms)
    
    # 同步发布
    results = syncer.sync_publish(
        md_file='article.md',
        title='测试文章',
        tags=['Python', '自动化', '效率工具']
    )
    
    print('发布结果:', results)

if __name__ == '__main__':
    main()