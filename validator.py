import hashlib
import hmac

ROLL_CHARS = 15  # 截取哈希值的前15个字符
ROLL_MAX = 100000  # 最大值为100000

def generate_roll(server_seed: str, client_seed: str, nonce: int) -> int:
    """
    计算出伪随机数 (roll) 的函数
    :param server_seed: 服务器种子
    :param client_seed: 客户端种子
    :param nonce: 用于保证每次哈希计算唯一性的计数器或时间戳
    :return: 伪随机数 (1 到 100000)
    """
    # 使用 HMAC-SHA512 生成哈希值
    message = f"{client_seed}-{nonce}"
    hash_object = hmac.new(server_seed.encode(), message.encode(), hashlib.sha512)
    hash_hex = hash_object.hexdigest()

    # 截取前 15 个字符作为子哈希
    sub_hash = hash_hex[:ROLL_CHARS]

    # 将子哈希转换为十六进制，并将其映射为十进制数
    roll_number = int(sub_hash, 16) % ROLL_MAX

    # 因为范围是 [0, 99999]，所以 +1 使其范围是 [1, 100000]
    return roll_number + 1

def calculate_public_hash(secret: str, salt: str) -> str:
    """
    计算公钥哈希，用于校验服务器种子
    :param secret: 服务器密钥
    :param salt: 密钥盐
    :return: 计算出的哈希值
    """
    return hashlib.sha256(f"{secret}{salt}".encode()).hexdigest()

# 测试代码
server_seed = "b1e09ba4298225e04682e44a0f95c1ad"
client_seed = "0x4babc432f015985c0c6f42177082fb4a6926436f"
nonce = 2
salt = "dc8b74025d9933e964453ed34acb4225"

# 生成的随机数
generated_roll = generate_roll(server_seed, client_seed, nonce)
print("Generated roll:", generated_roll)

# 计算公钥哈希
public_hash = calculate_public_hash(server_seed, salt)
print("Calculated Public Hash:", public_hash)
