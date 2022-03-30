using Microsoft.EntityFrameworkCore;

namespace ServerExam.Models
{
    internal class DB { }

    public class DbContentCore : DbContext
    {
        public DbContentCore(DbContextOptions<DbContentCore> options) : base(options) { }
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder) { }
        protected override void OnModelCreating(ModelBuilder modelBuilder) { base.OnModelCreating(modelBuilder); }
    }
}
