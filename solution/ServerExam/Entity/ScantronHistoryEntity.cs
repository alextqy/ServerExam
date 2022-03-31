using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class ScantronHistoryEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        /// <summary>
        /// 标题
        /// </summary>
        [JsonPropertyName("QuestionTitle")]
        public string QuestionTitle { get; set; }

        /// <summary>
        /// 标题代码
        /// </summary>
        [JsonPropertyName("QuestionCode")]
        public string QuestionCode { get; set; }

        /// <summary>
        /// 试题类型
        /// </summary>
        [JsonPropertyName("QuestionType")]
        public int QuestionType { get; set; }

        /// <summary>
        /// 试题状态 1正常 2禁用
        /// </summary>
        [JsonPropertyName("QuestionState")]
        public int QuestionState { get; set; }

        /// <summary>
        /// 是否人工阅卷 1否 2是
        /// </summary>
        [JsonPropertyName("Marking")]
        public int Marking { get; set; }

        /// <summary>
        /// 知识点ID
        /// </summary>
        [JsonPropertyName("KnowledgeID")]
        public int KnowledgeID { get; set; }

        /// <summary>
        /// 试题描述
        /// </summary>
        [JsonPropertyName("Describe")]
        public string Describe { get; set; }

        /// <summary>
        /// 试题附件
        /// </summary>
        [JsonPropertyName("Attachment")]
        public string Attachment { get; set; }

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
        /// 答题卡得分
        /// </summary>
        [JsonPropertyName("Score")]
        public decimal Score { get; set; }

        /// <summary>
        /// 报名ID
        /// </summary>
        [JsonPropertyName("ExamID")]
        public int ExamID { get; set; }

        /// <summary>
        /// 大标题内容
        /// </summary>
        [JsonPropertyName("HeadlineContent")]
        public string HeadlineContent { get; set; }

        public ScantronHistoryEntity()
        {
            this.ID = 0;
            this.QuestionTitle = "";
            this.QuestionCode = "";
            this.QuestionType = 0;
            this.QuestionState = 0;
            this.Marking = 0;
            this.KnowledgeID = 0;
            this.Describe = "";
            this.Attachment = "";
            this.CreateTime = 0;
            this.UpdateTime = 0;
            this.Score = 0;
            this.ExamID = 0;
            this.HeadlineContent = "";
        }
    }
}
