using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ServerExam.Entity
{
    public class SubjectEntity
    {
        [Key]
        [JsonPropertyName("ID")]
        public int ID { get; set; }

        public SubjectEntity()
        {
        }
    }
}
