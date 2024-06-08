from crawler.tools.handle import *
from help import *
import sys


def main():
    if len(sys.argv) != 2:
        print(f'{script_info()}\b{help()}')
        sys.exit(1)
    
    option = sys.argv[1]
    
    if option == '--help':
        print(help())
    elif option == '--version':
        print(script_info())
    elif option == '--crawler':
        handle_crawler()
    elif option == '--products-sitemap':
        handle_products_sitemap()
    elif option == '--products-list':
        handle_products_list()
    elif option == '--product-info':
        handle_products_info()
    elif option == '--test':
        handle_test()
    elif option == '--serve':
        from crawler.tools.server import run_server
        run_server()
    else:
        print(f"Unknown option: {option}\n{help()}")

if __name__ == "__main__":
    main()