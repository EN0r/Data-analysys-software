using Microsoft.Office.Core;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.OleDb;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Timers;
using System.Windows.Forms;
namespace Data_analysys
{
    public partial class Form1: Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        public DataTable createDTFromFile(string directory)
        {
            int rowCount = 0;
            StreamReader reader = new StreamReader(directory);
            string line = "";
            DataTable dt = new DataTable();
            while ((line = reader.ReadLine()) != null)
            {
                string[] tsv = line.Split(new char[] { '\t' }).ToArray();
                //remove any end spaces from data
                tsv = tsv.Select(x => x.Trim()).ToArray();

                if (++rowCount == 1)
                {
                    foreach (string colName in tsv)
                    {
                        dt.Columns.Add(colName, typeof(string));
                    }
                }
                else
                {
                    dt.Rows.Add(tsv);
                }
            }
            return dt;
        }
        /*
            Okay sooooo what i need to do is create a report function
            to export a list of the most common countries that are on the list.
            also the average price of whats spent per country.
            Also the most common car rented based on their vehicle
            
            Problem statement:
                The value numbers should be presented in GBP (I have included the values for conversion but have not completed this step.) 
                Make sure the dates are displayed correctly (including times if you want to use them)
                Use filters/slicers to allow users to interact with your findings
                A final consideration would be to look closely at the Brokers. Enjoy does exist in this list. This means that our prices here are in a different category to others. How might you deal with that? 

            Action plan:
            Use streamlit to visualise this data and use this software as a backend tool to generate reports to be used by the frontend python software.
            For the value numbers i will count the rows from the top of the colum with value and add a pound sign at the start of each using a for loop. Probably need to use a new thread for the operation for speed.
         */
        private void filebrowser_Click(object sender, EventArgs e)
        {
             OpenFileDialog fileDialog = new OpenFileDialog();

            fileDialog.Filter = "TSV Files (*.tsv)|*.tsv";
            if (fileDialog.ShowDialog() == DialogResult.OK)
            {
                string selectedFilePath = fileDialog.FileName;
                Console.WriteLine($"Selected File: {selectedFilePath}");
                MessageBox.Show("File opened succesfully!");
                groupBox1.Text = "Currently viewing: " + selectedFilePath;
            }
            var timer = new Stopwatch();

            dataGridView1.DataSource = createDTFromFile(fileDialog.FileName);
        }

        private void tableLayoutPanel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void toolStrip1_ItemClicked(object sender, ToolStripItemClickedEventArgs e)
        {

        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }
    }
}
