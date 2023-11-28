from random import randrange

CITY_NUM = 50   #城市数量


# 使用随机函数初始化城市的位置，并写入data.txt中
def main():
    city_location = []
    for _ in range(CITY_NUM):
        city = [randrange(500), randrange(500)]
        # 防止两个城市处于相同的位置
        while city in city_location:
            city = [randrange(100), randrange(100)]
        city_location.append(city)
    with open("data.txt", "w") as file:
        file.write(f"{CITY_NUM}\n")
        for i in range(len(city_location)):
            file.write(f"{i+1} {city_location[i][0]} {city_location[i][1]}\n")


if __name__ == "__main__":
    main()
