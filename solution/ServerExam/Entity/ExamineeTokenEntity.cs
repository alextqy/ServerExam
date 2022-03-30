using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class ExamineeTokenEntity : Base
    {
        /// <summary>
        /// 考生Token
        /// </summary>
        [Column(TypeName = "varchar(128)")]
        [MaxLength(128)]
        [JsonPropertyName("Token")]
        public string Token { get; set; }

        /// <summary>
        /// 报名ID
        /// </summary>
        [Column(TypeName = "int(10)")]
        [MaxLength(10)]
        [JsonPropertyName("ExamID")]
        public string ExamID { get; set; }

        public ExamineeTokenEntity()
        {
            this.Token = "";
            this.ExamID = 0;
        }
    }
}
