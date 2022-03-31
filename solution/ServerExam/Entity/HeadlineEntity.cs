using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class HeadlineEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        /// <summary>
        /// 内容
        /// </summary>
        [JsonPropertyName("Content")]
        public string Content { get; set; }

        /// <summary>
        /// 内容代码
        /// </summary>
        [JsonPropertyName("ContentCode")]
        public string ContentCode { get; set; }

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

        public HeadlineEntity()
        {
            this.ID = 0;
            this.Content = "";
            this.ContentCode = "";
            this.CreateTime = 0;
            this.UpdateTime = 0;
        }
    }
}
