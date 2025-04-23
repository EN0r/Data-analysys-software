using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Data_analysys
{
    public partial class analysysForm: Form
    {
        public analysysForm()
        {
            InitializeComponent();
        }
        public void setDVT(DataGridView dvt)
        {
            insightDVT.DataSource = dvt;
        }
        private void button1_Click(object sender, EventArgs e)
        {
            
        }

        private void insightDVT_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            
        }
    }
}
