from Entity.BaseEntity import BaseEntity


# 管理员
class ManagerEntity(BaseEntity):
    Account = ''  # 账号
    PWD = ''  # 密码
    Name = ''  # 名称
    State = 0  # 状态 1正常 2禁用
    Permission = 0  # 权限 9 ~ 1 从高到低
    UpdateTime = 0  # 更新时间
    Token = ''  # Token
