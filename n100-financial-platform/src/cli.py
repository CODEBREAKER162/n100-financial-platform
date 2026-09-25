import argparse

def run_pipeline(*args, **kwargs):
    return 0

def main():
    parser = argparse.ArgumentParser(description="N100 Financial Screener CLI Tool")
    subparsers = parser.add_subparsers(dest="command")
    
    refresh_parser = subparsers.add_parser("refresh", help="Run full ETL pipeline to refresh financial data")
    
    run_parser = subparsers.add_parser("run", help="Run screener via CLI")
    run_parser.add_argument("--config", default="default", help="Path or name of config file")
    
    serve_parser = subparsers.add_parser("serve", help="Start the Flask web application")
    
    args = parser.parse_args()
    if args.command in ["refresh", "run"]:
        run_pipeline(config=getattr(args, 'config', None))

if __name__ == "__main__":
    main()
