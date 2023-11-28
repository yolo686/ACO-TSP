from math import sqrt, pow, inf
import numpy as np
import matplotlib.pyplot as plt


class ACO:
    def __init__(self, num_city, data):
        self.num_city = num_city  # 城市数量
        self.location = data  # 城市的位置
        self.num_ant = 200  # 蚂蚁数量
        self.alpha = 1  # 信息素重要程度因子
        self.beta = 6  # 启发函数重要因子
        self.p = 0.8  # 信息素残留系数
        self.Q = 50  # 常量系数
        self.iter_max = 200  # 最大迭代次数
        self.dis_mat = self.compute_dis_mat()  # 距离矩阵
        self.Tau_mat = np.ones([num_city, num_city])  # 信息素矩阵
        self.Eta_mat = 200. / self.dis_mat  # 启发式函数
        self.table = [[0 for _ in range(num_city)] for _ in range(self.num_ant)]  # 蚁群的路径

    # 计算城市之间的距离矩阵
    def compute_dis_mat(self):
        dis_mat = np.zeros((self.num_city, self.num_city))
        for i in range(self.num_city):
            a = self.location[i]
            for j in range(self.num_city):
                b = self.location[j]
                dis_mat[i][j] = sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))
                if i == j:  # 防止计算启发函数时,0做分母
                    dis_mat[i][j] = 1
        return dis_mat

    # 轮盘赌选择
    def rand_choose(self, p):
        x = np.random.rand()*sum(p)
        for i, t in enumerate(p):
            x -= t
            if x <= 0:
                return i

    # 生成蚁群
    def get_ants(self):
        for i in range(self.num_ant):
            start = np.random.randint(self.num_city - 1)
            self.table[i][0] = start
            unvisit = list([x for x in range(self.num_city) if x != start])
            current = start
            j = 1
            while len(unvisit) != 0:
                P = []
                # 通过信息素计算城市之间的转移概率
                for v in unvisit:
                    P.append(self.Tau_mat[current][v] ** self.alpha * self.Eta_mat[current][v] ** self.beta)
                # 轮盘赌选择下一个城市
                index = self.rand_choose(P)
                current = unvisit[index]
                self.table[i][j] = current
                unvisit.remove(current)
                j += 1

    # 计算整个蚁群每个蚂蚁的路径长度
    def get_pathLen(self):
        paths = []
        for path in self.table:
            length = 0  # 每个蚂蚁走完一圈的路径长度
            for i in range(self.num_city - 1):
                length += self.dis_mat[int(path[i])][int(path[i + 1])]
            length += self.dis_mat[int(path[0])][int(path[self.num_city-1])]
            paths.append(length)
        return paths

    # 更新信息素  Ant-Circle System模型
    def update_Tau(self):
        delta_tau = np.zeros([self.num_city, self.num_city])
        paths = self.get_pathLen()
        for i in range(self.num_ant):
            for j in range(self.num_city - 1):
                a = self.table[i][j]
                b = self.table[i][j + 1]
                delta_tau[a][b] = self.Q / paths[i]
            a = self.table[i][0]
            b = self.table[i][self.num_city - 1]
            delta_tau[a][b] = self.Q / paths[i]
            self.Tau_mat = self.p * self.Tau_mat + delta_tau

    # 更新信息素  Ant- Quantity System模型
    # def update_Tau(self):
    #     delta_tau = np.zeros([self.num_city, self.num_city])
    #     for i in range(self.num_ant):
    #         for j in range(self.num_city - 1):
    #             a = self.table[i][j]
    #             b = self.table[i][j + 1]
    #             delta_tau[a][b] = self.Q / self.dis_mat[a][b]
    #         a = self.table[i][0]
    #         b = self.table[i][self.num_city - 1]
    #         delta_tau[a][b] = self.Q / self.dis_mat[a][b]
    #     self.Tau_mat = self.p * self.Tau_mat + delta_tau

    def run(self):
        best_length = inf  # 最短路径初始化为无穷大
        best_path = []
        for cnt in range(self.iter_max):  # 迭代终止条件
            # 生成新的蚁群
            self.get_ants()
            # 取该蚁群的最优解
            paths = self.get_pathLen()
            tmp_length = min(paths)
            tmp_path = self.table[paths.index(tmp_length)]
            # 更新最优解
            if tmp_length < best_length:
                best_length = tmp_length
                best_path = tmp_path.copy()
            # 更新信息素
            self.update_Tau()
            # 打印每次迭代获得的最短路径长度
            print(cnt + 1, best_length)
        best_path.append(best_path[0])
        print("蚁群算法结果:")
        print(f"length: {best_length}")
        print(f"path: {best_path}")
        location = np.array(self.location)
        data = []
        for i in best_path:
            data.append(self.location[i])
        data = np.array(data)
        # 绘制图像
        plt.scatter(location[:, 0], location[:, 1])
        plt.plot(data[:, 0], data[:, 1])
        plt.title(f"ACO-TSP Solver: iterating {self.iter_max} times")
        plt.show()
        return best_length, best_path


# 从data.txt中读取数据
def read_data():
    with open("data.txt", "r") as file:
        num_city = int(file.readline().strip())
        data = []
        for line in file.readlines():
            city = line.strip().split(" ")[1:]
            city = [int(x) for x in city]
            data.append(city)
    return num_city, data


def main():
    num_city, data = read_data()
    aco = ACO(num_city, data)  # 将ACO例化
    aco.run()


if __name__ == "__main__":
    main()
