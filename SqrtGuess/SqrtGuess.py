import math
from fractions import Fraction
from itertools import product

def is_square_free(n):
    """检查是否为平方自由的正整数且不等于1"""
    if n <= 1:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % (i*i) == 0:
            return False
    return True

def generate_fractions(num_range, den_range):
    """生成最简分数集合"""
    fractions = set()
    for num in range(num_range[0], num_range[1]+1):
        for den in range(den_range[0], den_range[1]+1):
            if den == 0:
                continue
            if math.gcd(num, den) == 1:
                fractions.add(Fraction(num, den))
    return fractions

def find_closest(target, a_range=(-20,20), b_range=(1,20), 
                c_range=(-20,20), d_range=(1,20), e_range=(2,20), n=5):
    # 生成有效e值
    valid_e = [e for e in range(e_range[0], e_range[1]+1) if is_square_free(e)]
    
    # 生成分数组合
    a_b_fractions = generate_fractions(a_range, b_range)
    c_d_fractions = generate_fractions(c_range, d_range)
    
    results = []
    for a_b, c_d, e in product(a_b_fractions, c_d_fractions, valid_e):
        try:
            # 计算表达式值
            value = float(a_b) + float(c_d) * math.sqrt(e)
            error = abs(value - target)
            
            # 记录参数
            results.append((
                error,
                a_b.numerator, a_b.denominator,
                c_d.numerator, c_d.denominator,
                e
            ))
        except:
            continue
    
    # 排序并取前n个
    results.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4], x[5]))
    return results[:n]

def format_result(result):
    """格式化输出结果"""
    error, a_num, a_den, c_num, c_den, e = result
    
    # 处理a/b部分
    a_part = f"{a_num}/{a_den}" if a_den != 1 else f"{a_num}"
    
    # 处理c/d√e部分
    if c_num == 0:
        return f"{a_part} (误差: {error:.6f})"
    
    c_part = f"{c_num}/{c_den}" if c_den != 1 else f"{c_num}"
    sqrt_part = f"√{e}"
    
    return f"{a_part} + {c_part}{sqrt_part} (误差: {error:.6f})"

# 交互界面
print("🔢 分数式实数近似工具 🔢")
target = float(input("请输入目标实数: "))
n = int(input("需要显示的结果数量: ") or 5)

# 执行搜索
results = find_closest(target, n=n)

# 显示结果
print("\n最佳匹配结果：")
for i, res in enumerate(results, 1):
    print(f"{i}. {format_result(res)}")