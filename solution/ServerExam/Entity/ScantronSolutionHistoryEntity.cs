using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class ScantronSolutionHistoryEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        /// <summary>
        /// 试题ID
        /// </summary>
        [JsonPropertyName("ScantronID")]
        public int ScantronID { get; set; }

        /// <summary>
        /// 选项
        /// </summary>
        [JsonPropertyName("Option")]
        public string Option { get; set; }

        /// <summary>
        /// 选项附件
        /// </summary>
        [JsonPropertyName("OptionAttachment")]
        public string OptionAttachment { get; set; }

        /// <summary>
        /// 正确答案
        /// </summary>
        [JsonPropertyName("CorrectAnswer")]
        public string CorrectAnswer { get; set; }

        /// <summary>
        /// 考生答案
        /// </summary>
        [JsonPropertyName("CandidateAnswer")]
        public string CandidateAnswer { get; set; }

        /// <summary>
        /// 得分比例
        /// </summary>
        [JsonPropertyName("ScoreRatio")]
        public decimal ScoreRatio { get; set; }

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

        public ScantronSolutionHistoryEntity()
        {
            this.ID = 0;
            this.ScantronID = 0;
            this.Option = "";
            this.OptionAttachment = "";
            this.CorrectAnswer = "";
            this.CandidateAnswer = "";
            this.ScoreRatio = 0;
            this.CreateTime = 0;
            this.UpdateTime = 0;
        }
    }
}
