using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class PaperRuleEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        /// <summary>
        /// 大标题ID
        /// </summary>
        [JsonPropertyName("HeadlineID")]
        public int HeadlineID { get; set; }

        /// <summary>
        /// 试题类型
        /// </summary>
        [JsonPropertyName("QuestionType")]
        public int QuestionType { get; set; }

        /// <summary>
        /// 试题数量
        /// </summary>
        [JsonPropertyName("QuestionNum")]
        public int QuestionNum { get; set; }

        /// <summary>
        /// 平均分
        /// </summary>
        [JsonPropertyName("AverageScore")]
        public decimal AverageScore { get; set; }

        /// <summary>
        /// 试卷ID
        /// </summary>
        [JsonPropertyName("PaperID")]
        public int PaperID { get; set; }

        /// <summary>
        /// 试卷规则状态 1正常 2禁用
        /// </summary>
        [JsonPropertyName("PaperRuleState")]
        public int PaperRuleState { get; set; }

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

        public PaperRuleEntity()
        {
            this.ID = 0;
            this.HeadlineID = 0;
            this.QuestionType = 0;
            this.QuestionNum = 0;
            this.AverageScore = 0;
            this.PaperID = 0;
            this.CreateTime = 0;
            this.UpdateTime = 0;
        }
    }
}
