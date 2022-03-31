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
        [JsonPropertyName("Token")]
        public string Token { get; set; }

        /// <summary>
        /// 报名ID
        /// </summary>
        [JsonPropertyName("ExamID")]
        public int ExamID { get; set; }

        public ExamineeTokenEntity()
        {
            this.Token = "";
            this.ExamID = 0;
        }
    }
}
