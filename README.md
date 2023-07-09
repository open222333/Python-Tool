# Python-Cerbort_Tool

```
生成 指令
```

## 用法

```bash
usage: main.py [-h] [-d {SOA,NS,A,AAAA,PTR,CNAME,MX}] [-c] [-r] [-R] [-C] [-e] [-s] [-S] [-T] [-m] [-t] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

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

## 常用

```bash
# 生成證書
python main.py -c -C -T -m

# 刷新證書
python main.py -r -m
```