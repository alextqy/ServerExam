using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class PaperEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        /// <summary>
        /// 试卷名称
        /// </summary>
        [JsonPropertyName("PaperName")]
        public string PaperName { get; set; }

        /// <summary>
        /// 科目ID
        /// </summary>
        [JsonPropertyName("SubjectID")]
        public int SubjectID { get; set; }

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
        /// 考试时长
        /// </summary>
        [JsonPropertyName("ExamDuration")]
        public int ExamDuration { get; set; }

        /// <summary>
        /// 试卷状态 1正常 2禁用
        /// </summary>
        [JsonPropertyName("PaperState")]
        public int PaperState { get; set; }

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

        public PaperEntity()
        {
            this.ID = 0;
            this.PaperName = "";
            this.SubjectID = 0;
            this.TotalScore = 0;
            this.PassLine = 0;
            this.ExamDuration = 0;
            this.PaperState = 0;
            this.CreateTime = 0;
            this.UpdateTime = 0;
        }
    }
}
