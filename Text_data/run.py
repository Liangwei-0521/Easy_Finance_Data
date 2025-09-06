import os
import sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import time
import random
from tqdm import tqdm
from Text_data.get_data import * 
from params import params_set, title_headers, title_cookies



def guba_info(
        guba_name:str, 
        page_num:int,
    ):
    
    # step 1: 获取单页贴文信息，返回List
    content_list = each_one_pager_info(
        guba_name=guba_name,
        page_num=page_num,
        cookies=title_cookies,
        headers=title_headers
    )

    # step 2：获取贴文正文内容和附加评论信息
    try:
        for item in tqdm(content_list):
            if item["贴吧名称"] == "上证指数吧":
                time.sleep(random.uniform(1, 3))
                content_cookies_0, content_headers_0, comment_cookies_0, comment_headers_0, comment_data_0, content_cookies_20, content_headers_20, content_params_20, comment_cookies_20, comment_headers_20 , comment_params_20 = params_set(
                    paper_id = item['贴文id'],
                    guba_name=guba_name,
                    writer_id=item['作者id'],
                    time_stamp=item['发表时间戳']
                )

                item['评论'] = []
                if item['贴文类型'] == 0:
                    # 正文信息(post_style = 0)
                    time.sleep(random.uniform(1, 3))
                    post_abstract = get_paper_content_style_0(
                        guba_name = guba_name,
                        paper_id = item['贴文id'],
                        cookies=content_cookies_0,
                        headers=content_headers_0

                    )
                    # 评论信息
                    time.sleep(random.uniform(1, 3))
                    comment_er = get_comment_from_style_0(guba_name=guba_name,
                                                        item_comment=item['评论'],
                                                        cookies=comment_cookies_0,
                                                        headers=comment_headers_0,
                                                        data=comment_data_0)

                if item['贴文类型']  == 20:
                    # 正文信息（post_style = 20)
                    time.sleep(random.uniform(1, 3))
                    post_abstract = get_paper_content_style_20(
                        params=content_params_20, 
                        cookies=content_cookies_20,
                        headers=content_headers_20
                    )
                    # 评论信息
                    time.sleep(random.uniform(1, 3))
                    comment_er = get_comment_from_style_20(params=comment_params_20, 
                                                        item_comment=item['评论'],
                                                        cookies=comment_cookies_20,
                                                        headers=comment_headers_20)

                item['正文'] = post_abstract

                # 存储 JSON 文件
                output_file = "guba.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(content_list, f, ensure_ascii=False, indent=2)

                print(content_list[-1])
    except Exception as e:
        print(e)
        
    return content_list


if __name__ == '__main__':

    total_num = 100
    for idx in range(total_num):
        pass 
    
    guba_info(
        guba_name='zssh000001',
        page_num=1
    )









