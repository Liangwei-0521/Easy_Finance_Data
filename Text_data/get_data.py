import re 
import json
import json5
import requests
import time
import random
from datetime import datetime, timedelta



def generate_timestamp_with_random_ms_offset() -> str:
    """
    获取当前时间，随机往前延 1-2 分钟，生成时间戳（秒）+ 随机毫秒
    """
    # 获取当前时间
    now = datetime.now()
    
    # 随机延前 60~120 秒
    offset_seconds = random.randint(60, 120)
    dt = now - timedelta(seconds=offset_seconds)
    
    # 转成 Unix 时间戳（秒）
    ts_seconds = int(time.mktime(dt.timetuple()))
    
    # 随机 3 位毫秒
    ms = random.randint(0, 999)
    
    # 拼接成完整时间戳字符串
    full_ts = f"{ts_seconds}{ms:03d}"
    return full_ts


# 获取单页评论标题info
def get_title_info(guba_name:str, page_num:int, cookies:dict, headers:dict):
    # 从html文件里获取var_parma list
    print("DEBUG guba_name:", guba_name, "page_num:", page_num)
    response = requests.get('https://guba.eastmoney.com/list,'+guba_name+'_'+str(page_num)+'.html', cookies=cookies, headers=headers)
    return response.text


# 处理
def page_info_process(html):
    # 用正则提取 article_list 里的 JSON
    pattern = re.compile(r"var\s+article_list\s*=\s*(\{.*?\});", re.S)
    match = pattern.search(html)

    if match:
        article_json_str = match.group(1)

        # 转成 Python dict
        try:
            article_data = json.loads(article_json_str)
            print("成功解析到 article_list!")
            # 打印前几个帖子标题
            for item in article_data.get("list", [])[:5]:
                print("标题:", item.get("title"), " 链接:", item.get("post_url"))
        except Exception as e:
            print("JSON 解析失败:", e)
    else:
        print("没有找到 article_list 变量")

    return article_data


def each_one_pager_info(guba_name:str, page_num:int, cookies:dict, headers:dict):
    # 1、get title information
    html = get_title_info(
        guba_name=guba_name,
        page_num=page_num,
        cookies=cookies,
        headers=headers
    )
    # 2、process the html
    page_content = page_info_process(
        html=html
    )

    content_list = []
    for item_writer in page_content['re']:
        # 一级信息
        writer = {
            '贴吧名称': item_writer['stockbar_name'],
            '贴文id': item_writer['post_id'],
            '贴文类型': item_writer['post_type'],
            '发布时间': item_writer['post_publish_time'],
            '发表时间戳': item_writer['post_source_id'],
            '贴文标题': item_writer['post_title'],
            '作者id': item_writer['user_id'],
            '作者名称': item_writer['user_nickname'],
            '阅读数': item_writer['post_click_count'],
            '评论数': item_writer['post_comment_count']
        }
        
        content_list.append(writer)

    return content_list


# 针对帖子正文的处理：'贴文类型': 0
def extract_post_article(html:str):
    """
    从 HTML 中提取单个 post_article 并返回 Python 字典
    """
    # 匹配 var post_article = {...}
    match = re.search(r"var\s+post_article\s*=\s*(\{.*\})\s*</script>", html, re.S)
    if not match:
        raise ValueError("未找到 post_article")
    js_content = match.group(1).strip()
    # 使用 json5 解析 JS 风格的 JSON（支持 true/false/null）
    post_data = json5.loads(js_content)
    return post_data


def request_paper_content_style_0(guba_name:str, paper_id:int, cookies:dict, headers:dict):
    response = requests.get('https://guba.eastmoney.com/news,'+guba_name+','+str(paper_id)+'.html', 
                        cookies=cookies, 
                        headers=headers)
    return response.text
    

def get_paper_content_style_0(guba_name:str, paper_id:int, cookies:dict, headers:dict):
    # step 1： 获取正文内容
    paper_content = request_paper_content_style_0(guba_name, paper_id, cookies, headers)
    # step 2： 解析正文内容
    post_data = extract_post_article(paper_content)
    return post_data['post_abstract']


def get_comment_from_style_0(guba_name:str,
                             item_comment:list,
                              cookies:dict, headers:dict, data:dict):
    # 需要data中传入贴文（paper）id
    response = requests.post(
    'https://guba.eastmoney.com/api/getData?code='+guba_name+'&path=reply/api/Reply/ArticleNewReplyList',
    cookies=cookies,
    headers=headers,
    data=data,
    )
    each_comment = response.json()

    if len(each_comment['re'])>0:

        for item in each_comment['re']:
            comment_er = {
                '评论id': item['reply_id'],
                '评论时间': item['reply_time'],
                '评论者id': item['reply_user']['user_id'],
                '评论者昵称': item['reply_user']['user_nickname'],
                '年限': item['reply_user']['user_age'],
                '地点':item['reply_ip_address'],
                '评论内容': item['reply_text']
            }

            if len(item['child_replys']) > 0 :
                # 评论回复
                comment_er['回复'] = []
                for item_sub_content in item['child_replys']:
                    comment_er['回复'].append( 
                        {
                        '回复id': item_sub_content['reply_id'],
                        '回复者id': item_sub_content['user_id'],
                        '回复者地址': item_sub_content['reply_ip_address'],
                        '回复时间': item_sub_content['reply_time'],
                        '回复内容':item_sub_content['reply_text']
                        }
                )
            else:
                comment_er['回复'] = None
            
            item_comment.append(comment_er)

    else:
        item_comment.append(None)

    # return comment_er


# 针对帖子正文的处理：'贴文类型': 20
def get_paper_content_style_20(params:dict, cookies:dict, headers:dict):
    response = requests.get('https://caifuhao.eastmoney.com/gbapi/AuthorCFHList', 
                        params=params, cookies=cookies, headers=headers)
    
    text = response.json()
    return text['re'][0]['post_content']


def parse_jsonp(text: str):
    """
    把 JSONP 格式字符串转换为 JSON 对象
    """
    # 提取括号里的内容
    match = re.search(r'^[^(]+\((.*)\)\s*$', text, re.S)
    if not match:
        raise ValueError("输入不是标准的 JSONP 格式")
    
    json_str = match.group(1)
    return json.loads(json_str)


def get_comment_from_style_20(params:dict, 
                              item_comment:list,
                              cookies:dict, headers:dict):
    
    response = requests.get(
        'https://gbapi.eastmoney.com/reply/JSONP/ArticleNewReplyList',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    data = parse_jsonp(response.text)
    if len(data['re']) >0:
        for item in data['re']:
            comment_er = {
                '评论id': item['reply_id'],
                '评论时间': item['reply_time'],
                '评论者id': item['reply_user']['user_id'],
                '评论者昵称': item['reply_user']['user_nickname'],
                '年限': item['reply_user']['user_age'],
                '地点': None, 
                '评论内容': item['reply_text']
            }

            if len(item['child_replys']) > 0 :
                comment_er['回复'] = []
                for item_sub_content in item['child_replys']:
                    comment_er['回复'].append( 
                        {
                        '回复id': item_sub_content['reply_id'],
                        '回复者id': item_sub_content['user_id'],
                        '回复者地址': item_sub_content['reply_ip_address'],
                        '回复时间': item_sub_content['reply_time'],
                        '回复内容':item_sub_content['reply_text']
                        }
                )
            else:
                comment_er['回复'] = None

            item_comment.append(comment_er)

    else:
        item_comment.append(None)

    # return comment_er



