using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class KnowledgeEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        /// <summary>
        /// 知识点名称
        /// </summary>
        [JsonPropertyName("KnowledgeName")]
        public string KnowledgeName { get; set; }

        /// <summary>
        /// 科目ID
        /// </summary>
        [JsonPropertyName("SubjectID")]
        public int SubjectID { get; set; }

        /// <summary>
        /// 知识点状态 1正常 2禁用
        /// </summary>
        [JsonPropertyName("SubjectState")]
        public int KnowledgeState { get; set; }

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

        public KnowledgeEntity()
        {
            this.ID = 0;
            this.KnowledgeName = "";
            this.SubjectID = 0;
            this.KnowledgeState = 0;
            this.CreateTime = 0;
            this.UpdateTime = 0;
        }
    }
}
