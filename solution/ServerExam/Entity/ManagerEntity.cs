using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class ManagerEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        /// <summary>
        /// 账号
        /// </summary>
        [JsonPropertyName("Account")]
        public string Account { get; set; }

        /// <summary>
        /// 密码
        /// </summary>
        [JsonPropertyName("PWD")]
        public string PWD { get; set; }

        /// <summary>
        /// 名字
        /// </summary>
        [JsonPropertyName("Name")]
        public string Name { get; set; }

        /// <summary>
        /// 状态 1正常 2禁用
        /// </summary>
        [JsonPropertyName("State")]
        public int State { get; set; }

        /// <summary>
        /// 权限
        /// </summary>
        [JsonPropertyName("Permission")]
        public int Permission { get; set; }

        /// <summary>
        /// 创建时间
        /// </summary>
        [JsonPropertyName("CreateTime")]
        public int CreateTime { get; set; }

        /// <summary>
        /// 更新时间
        /// </summary>
        [JsonPropertyName("UpdateTime")]
        public int UpdateTime { get; set; }

        /// <summary>
        /// Token
        /// </summary>
        [JsonPropertyName("Token")]
        public string Token { get; set; }

        public ManagerEntity()
        {
            this.ID = 0;
            this.Account = "";
            this.PWD = "";
            this.Name = "";
            this.State = 0;
            this.Permission = 0;
            this.CreateTime = 0;
            this.UpdateTime = 0;
            this.Token = "";
        }
    }
}
