using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class SysLogEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        /// <summary>
        /// 日志类型
        /// </summary>
        [JsonPropertyName("Type")]
        public int Type { get; set; }

        /// <summary>
        /// 管理员ID
        /// </summary>
        [JsonPropertyName("ManagerID")]
        public int ManagerID { get; set; }

        /// <summary>
        /// 描述
        /// </summary>
        [JsonPropertyName("Describe")]
        public string Describe { get; set; }

        /// <summary>
        /// 
        /// </summary>
        [JsonPropertyName("CreateTime")]
        public int CreateTime { get; set; }

        /// <summary>
        /// IP地址
        /// </summary>
        [JsonPropertyName("IP")]
        public string IP { get; set; }

        public SysLogEntity()
        {
            this.ID = 0;
            this.Type = 0;
            this.ManagerID = 0;
            this.Describe = "";
            this.CreateTime = 0;
            this.IP = "";
        }
    }
}
