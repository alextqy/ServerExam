using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class SubjectEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        /// <summary>
        /// 科目名称
        /// </summary>
        [JsonPropertyName("SubjectName")]
        public string SubjectName { get; set; }

        /// <summary>
        /// 科目代码
        /// </summary>
        [JsonPropertyName("SubjectCode")]
        public string SubjectCode { get; set; }

        /// <summary>
        /// 科目状态 1正常 2禁用
        /// </summary>
        [JsonPropertyName("SubjectState")]
        public int SubjectState { get; set; }

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

        public SubjectEntity()
        {
            this.ID = 0;
            this.SubjectName = "";
            this.SubjectCode = "";
            this.SubjectState = 0;
            this.CreateTime = 0;
            this.UpdateTime = 0;
        }
    }
}
