# Python-Cerbort_Tool

```
生成 cerbort 指令
```

## 目錄

- [Python-Cerbort\_Tool](#python-cerbort_tool)
	- [目錄](#目錄)
	- [參考資料](#參考資料)
- [用法](#用法)
	- [main-ssl\_command.py - 根據json檔，生成指令](#main-ssl_commandpy---根據json檔生成指令)
	- [main-txt.py - 根據txt檔，解析郵件格式並生成域名證書相關指令](#main-txtpy---根據txt檔解析郵件格式並生成域名證書相關指令)
	- [main-domain\_encode.py - 批量域名轉碼（編碼）punycode格式](#main-domain_encodepy---批量域名轉碼編碼punycode格式)
	- [main-nameserver.py - 根據 nginx conf 設定檔名, 回傳匹配指定 ns 的 domain](#main-nameserverpy---根據-nginx-conf-設定檔名-回傳匹配指定-ns-的-domain)
	- [main-scp.py - 批量傳送檔案(未完成)](#main-scppy---批量傳送檔案未完成)
- [常用](#常用)

## 參考資料

[]()

# 用法

## main-ssl_command.py - 根據json檔，生成指令

```json
// conf/domains.json 說明
[
  {
    "execute": false, // 是否執行
    "cloudflare_cli": "", // 指定 cli.ini設定檔
    "domains": "", // 要執行的域名 格式: test1.com,test2.com
    "refer_domain": "", // 參照域名
    "note": "" // 筆記
  },
  {
    "execute": false,
    "cloudflare_cli": "",
    "domains": "",
    "refer_domain": "",
    "note": ""
  }
]

```

```bash
# 根據 .conf/domains.json 生成指令
usage: main.py [-h] [-d {SOA,NS,A,AAAA,PTR,CNAME,MX}] [-c] [-r] [-R] [-C] [-e] [-s] [-S] [-T] [-m] [-t] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

根據json檔，生成指令

options:
  -h, --help            show this help message and exit

生成command功能:
  -d {SOA,NS,A,AAAA,PTR,CNAME,MX}, --dig_check_command {SOA,NS,A,AAAA,PTR,CNAME,MX}
                        生成 產生dig檢查record 類型指令串列
  -c, --create_ssl_command
                        生成 產生新證書certbot指令串列
  -r, --renew_ssl_command
                        生成 刷新證書certbot指令串列
  -R, --revoke_ssl_command
                        生成 註銷證書certbot指令串列
  -C, --cp_nginx_config_command
                        生成 複製 nginx conf 指令串列
  -e, --remove_conf_command
                        生成 刪除 nginx config 指令串列
  -s, --show_ssl_certificates_command
                        生成 顯示證書資料夾指令串列
  -S, --show_nginx_configs_command
                        生成 查找 nginx config指令串列
  -T, --create_test_url
                        生成 測試網址

顯示command功能:
  -m, --print_command   終端機印出指令
  -t, --generate_txt    產生txt檔記錄指令
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
```

## main-txt.py - 根據txt檔，解析郵件格式並生成域名證書相關指令

```bash
# 設定輸入資料的txt路徑 預設值 target.txt
# TXT_PATH=

usage: main-txt.py [-h] --cli CLI [-m] [-t] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

根據txt檔，解析郵件格式並生成域名證書相關指令

options:
  -h, --help            show this help message and exit

生成command功能:
  --cli CLI             指定cli檔

顯示command功能:
  -m, --print_command   終端機印出指令
  -t, --generate_txt    產生txt檔記錄指令
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
```

## main-domain_encode.py - 批量域名轉碼（編碼）punycode格式

```bash
usage: main-domain_encode.py [-h] [-f FILE_PATH] [-d OUTPUT]

批量域名轉碼（編碼） punycode格式

options:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file_path FILE_PATH
                        指定解析txt檔路徑
  -d OUTPUT, --output OUTPUT
                        指定輸出結果文檔路徑
```

## main-nameserver.py - 根據 nginx conf 設定檔名, 回傳匹配指定 ns 的 domain

```json
// ns_info.json
[
  {
    "execute": false, // 是否參與比對
    "name":"", // 名稱
    "ns":"" // ns 格式: test1.com,test2.com
  }
]
```

```bash
usage: main-nameserver.py [-h] [-o OUTPUT_FILENAME]

根據 nginx conf 設定檔名, 回傳匹配指定 ns 的 domain

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FILENAME, --output_filename OUTPUT_FILENAME
                        輸出檔名稱
```

## main-scp.py - 批量傳送檔案(未完成)

```bash
usage: main-scp.py [-h] [-l LOG_LEVEL] [-t TEST]

批量傳送檔案

options:
  -h, --help            show this help message and exit
  -l LOG_LEVEL, --log_level LOG_LEVEL
                        設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
  -t TEST, --test TEST  是否為測試
```

# 常用

```bash
# 生成證書
python main-ssl_command.py -c -C -T -m

# 刷新證書
python main-ssl_command.py -r -m

# 解析 txt檔產生指令
python main-txt.py --cli sample -m
```