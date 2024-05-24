import redis

def main():
    redis_client = redis.Redis(host='localhost',
                               port=6379)
    redis_client.set('prev-data', '123')
    print(redis_client.get('prev-data').decode())

    redis_client.close()

if __name__ == '__main__':
    main()