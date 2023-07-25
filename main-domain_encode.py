from src.tool import domain_encode


if __name__ == "__main__":
    with open('target.txt', 'r') as f:
        domains = f.read().split('\n')

    with open('output/domain_encode.txt', 'a') as f:
        for domain in domains:
            encode_domain = domain_encode(domain)
            f.write(f'{domain} {encode_domain}\n')
