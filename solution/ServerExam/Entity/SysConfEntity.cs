using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class SysConfEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        /// <summary>
        /// 配置类型
        /// </summary>
        [JsonPropertyName("Type")]
        public int Type { get; set; }

        /// <summary>
        /// 键
        /// </summary>
        [JsonPropertyName("Key")]
        public string Key { get; set; }

        /// <summary>
        /// 值
        /// </summary>
        [JsonPropertyName("Value")]
        public string Value { get; set; }

        /// <summary>
        /// 配置描述
        /// </summary>
        [JsonPropertyName("Describe")]
        public string Describe { get; set; }

        public SysConfEntity()
        {
            this.ID = 0;
            this.Type = 0;
            this.Key = "";
            this.Value = "";
            this.Describe = "";
        }
    }
}
