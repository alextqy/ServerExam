using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class ExamInfoEntity
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
        /// 准考证号
        /// </summary>
        [JsonPropertyName("ExamNo")]
        public string ExamNo { get; set; }

        /// <summary>
        /// 总分
        /// </summary>
        [JsonPropertyName("TotalScore")]
        public decimal TotalScore { get; set; }

        /// <summary>
        /// 及格线
        /// </summary>
        [JsonPropertyName("PassLine")]
        public decimal PassLine { get; set; }

        /// <summary>
        /// 实际得分
        /// </summary>
        [JsonPropertyName("ActualScore")]
        public decimal ActualScore { get; set; }

        /// <summary>
        /// 考试时长
        /// </summary>
        [JsonPropertyName("ExamDuration")]
        public int ExamDuration { get; set; }

        /// <summary>
        /// 开始时间
        /// </summary>
        [JsonPropertyName("StartTime")]
        public int StartTime { get; set; }

        /// <summary>
        /// 结束时间
        /// </summary>
        [JsonPropertyName("EndTime")]
        public int EndTime { get; set; }

        /// <summary>
        /// 实际考试时长
        /// </summary>
        [JsonPropertyName("ActualDuration")]
        public decimal ActualDuration { get; set; }

        /// <summary>
        /// 通过状态 1否 2是
        /// </summary>
        [JsonPropertyName("Pass")]
        public int Pass { get; set; }

        /// <summary>
        /// 联系方式
        /// </summary>
        [JsonPropertyName("ContactInfo")]
        public string ContactInfo { get; set; }

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

        public ExamInfoEntity()
        {
            this.ID = 0;
            this.SubjectName = "";
            this.ExamNo = "";
            this.TotalScore = 0;
            this.PassLine = 0;
            this.ActualScore = 0;
            this.ExamDuration = 0;
            this.StartTime = 0;
            this.EndTime = 0;
            this.ActualDuration = 0;
            this.Pass = 0;
            this.ContactInfo = "";
            this.CreateTime = 0;
            this.UpdateTime = 0;
        }
    }
}
