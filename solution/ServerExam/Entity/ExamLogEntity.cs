using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class ExamLogEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        /// <summary>
        /// 科目名称
        /// </summary>
        [JsonPropertyName("Type")]
        public int Type { get; set; }

        /// <summary>
        /// 准考证号
        /// </summary>
        [JsonPropertyName("ExamNo")]
        public string ExamNo { get; set; }

        /// <summary>
        /// 描述
        /// </summary>
        [JsonPropertyName("Describe")]
        public string Describe { get; set; }

        /// <summary>
        /// 创建时间
        /// </summary>
        [JsonPropertyName("CreateTime")]
        public int CreateTime { get; set; }

        /// <summary>
        /// 客户端IP
        /// </summary>
        [JsonPropertyName("IP")]
        public string IP { get; set; }

        public ExamLogEntity()
        {
            this.ID = 0;
            this.Type = 0;
            this.ExamNo = "";
            this.Describe = "";
            this.CreateTime = 0;
            this.IP = "";
        }
    }
}
