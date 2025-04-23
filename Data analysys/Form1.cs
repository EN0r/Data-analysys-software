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
using System.Net.NetworkInformation;
using System.Reflection;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Timers;
using System.Windows.Forms;
/*
 * There's alot to improve here especially exeption handling using try and catch.
 * Being new to c# ive learnt quite alot but in the time constraints i still have alot to learn as it is different to my usual projects.
 */
namespace Data_analysys
{
    public partial class Form1: Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        private string[] dataTableRAW;
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
                dataTableRAW = tsv;
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

        //                                 0    1    2
        private string[] currencies =   {  "£",   "€",  "$"   };
        private string[] currencyCodestr = { "GBP", "EUR", "USD" };

        private void getRowAttributes(DataGridView _dgv) // probably should be ran in a thread tbh
        {
            foreach (DataGridViewColumn col in _dgv.Columns) // ew nested for loops :(
            {
                // probably need to check if row has text
                //MessageBox.Show(Convert.ToString(r.Cells.Count));
                comboBox1.Items.Add(col.Name);
            }
        }

        public void setMoneyRows(DataGridView _dgv)
        {
            foreach(DataGridViewRow r in _dgv.Rows)
            {
                string currencyCode = Convert.ToString(r.Cells[15].Value);
                if(currencyCode == currencyCodestr[1]) // could use a switch case with enumeration values. But in this case i think if statements can be quicker with this state of data
                {
                    r.Cells[16].Value = currencies[1] + r.Cells[16].Value;
                    r.Cells[17].Value = currencies[0] + r.Cells[17].Value;
                    r.Cells[18].Value = currencies[0] + r.Cells[18].Value;
                } else if(currencyCode == currencyCodestr[0])
                {
                    r.Cells[16].Value = currencies[0] + r.Cells[16].Value;
                    r.Cells[17].Value = currencies[0] + r.Cells[17].Value;
                    r.Cells[18].Value = currencies[0] + r.Cells[18].Value;
                }
                // need to count vehicle type. Maybe make an array and store the first vehicle found and if the vehicle is not the first found add to array
            }
        }

        public Dictionary<string, int> CountOccurrences(DataGridView dgv, string columnName)
        {
            Dictionary<string, int> counts = new Dictionary<string, int>();

            foreach (DataGridViewRow row in dgv.Rows)
            {
                string value = row.Cells[columnName].Value?.ToString() ?? ""; // Handle null values safely

                if (counts.ContainsKey(value))
                {
                    counts[value]++;
                }
                else
                {
                    counts.Add(value, 1);
                }
            }

            return counts;
        }

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
            getRowAttributes(dataGridView1);
            setMoneyRows(dataGridView1);
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
        private void removeEmptyRows(DataGridView dgv,DataGridViewColumn col)
        {
            List<DataGridViewRow> rowsToRemove = new List<DataGridViewRow>();

            foreach (DataGridViewRow row in dgv.Rows)
            {
                if (string.IsNullOrWhiteSpace(row.Cells[col.Name].Value?.ToString()))
                {
                    rowsToRemove.Add(row);
                }
            }

            foreach (DataGridViewRow rowToRemove in rowsToRemove)
            {
                dgv.Rows.Remove(rowToRemove);
            }
        }

        private DataTable generateDataTable(DataGridView originTable)
        {
            DataTable dt = new DataTable();
            List<int> cellIds = new List<int>();

            foreach (var addedItem in checkedListBox1.CheckedItems)
            {
                foreach (DataGridViewColumn col in originTable.Columns)
                {
                    if (col.Name == addedItem.ToString())
                    {
                        dt.Columns.Add(addedItem.ToString());
                        cellIds.Add(col.Index);
                        break;
                    }
                }
            }



            foreach (DataGridViewRow row in originTable.Rows)
            {
                DataRow newRow = dt.NewRow();

                for (var i = 0; i < cellIds.Count; i++)
                {
                    newRow[i] = row.Cells[cellIds[i]].Value;
                }

                dt.Rows.Add(newRow);
            }

            // false data cleanup

            return dt;
        }

        private double CalculateAverage(DataTable dt, string columnName)
        {
            double sum = 0;
            int count = 0;

            foreach (DataRow row in dt.Rows)
            {
                object value = row[columnName];

                if (value != DBNull.Value && double.TryParse(value?.ToString(), out double numValue))
                {
                    sum += numValue;
                    count++;
                }
            }

            if (count == 0)
            {
                // Handle the case where there are no valid numeric values
                return 0; // Or throw an exception, depending on your desired behavior
            }

            return sum / count;
        }

        private void ExportToTSV(DataGridView dgv, string filePath, string fileName) // probably need to add a exeption to handle if a file already exists but time limitations.
        {
            StringBuilder sb = new StringBuilder();
            FileStream fileStream = File.Create(filePath + "\\" + fileName + ".tsv");
            foreach (DataGridViewColumn col in dgv.Columns)
            {
                sb.Append(col.HeaderText);
                sb.Append("\t"); // tab delimiter
            }
            sb.AppendLine();

            // Add data rows
            foreach (DataGridViewRow row in dgv.Rows)
            {
                foreach (DataGridViewCell cell in row.Cells)
                {
                    sb.Append(cell.Value?.ToString() ?? ""); // final cleanup? had to google around to figure out this expression :(
                    sb.Append("\t");
                }
                sb.AppendLine();
            }

            File.WriteAllText(filePath, sb.ToString());
        }

        private double CalculateAverageFromDataGridView(DataGridView dgv, string columnName)
        {
            DataTable dt = new DataTable(); // temp dt

            foreach (DataGridViewColumn col in dgv.Columns)
            {
                dt.Columns.Add(col.Name);
            }

            foreach (DataGridViewRow row in dgv.Rows)
            {
                DataRow newRow = dt.NewRow();

                for (int i = 0; i < dgv.ColumnCount; i++)
                {
                    newRow[i] = row.Cells[i].Value;
                }

                dt.Rows.Add(newRow);
            }

            return CalculateAverage(dt, columnName); 
        }

        private void displayCountsInDataGridView(Dictionary<string, int> itemCounts)
        {
            dgvCounts.Columns.Add("Value", "Value"); // Column for the unique values
            dgvCounts.Columns.Add("Count", "Count"); // Column for the counts
            foreach (var kvp in itemCounts)
            {
                dgvCounts.Rows.Add(kvp.Key, kvp.Value);
            }
        }
        

        private void button1_Click(object sender, EventArgs e) // this can be table generated from the button and selections of the checkedListBox1
        {
            dataGridView2.DataSource = generateDataTable(dataGridView1);
        }

        private void button2_Click(object sender, EventArgs e) { 
            if(comboBox1.SelectedItem != null)
                checkedListBox1.Items.Add(comboBox1.SelectedItem); 
        }

        private void button3_Click(object sender, EventArgs e) 
        {
            if (comboBox1.SelectedItem != null)
                checkedListBox1.Items.Remove(comboBox1.SelectedItem);
        }

        private void button5_Click(object sender, EventArgs e)
        {
            analysysForm newForm = new analysysForm();
            newForm.Show();
        }



        private void button6_Click(object sender, EventArgs e)
        {
            Dictionary<string, int> itemCounts = CountOccurrences(dataGridView2, textBox1.Text);
            displayCountsInDataGridView(itemCounts);
        }

        private void button7_Click(object sender, EventArgs e)
        {
            dgvCounts.DataSource = null;
            dgvCounts.Rows.Clear();
        }

        private void button8_Click(object sender, EventArgs e)// calculate averages
        {
            double averagePrice = CalculateAverageFromDataGridView(dataGridView2, textBox1.Text);

            if (textBox1.Text != "") // Check for valid result
            {
                textBox2.Text = "Average Price: " + Convert.ToString(averagePrice);
            }
        }

        private void dgvCounts_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void button4_Click(object sender, EventArgs e) // Export generated selections
        {

        }

        private void button10_Click(object sender, EventArgs e) // Export insights
        {

        }

        private void button9_Click(object sender, EventArgs e) // export all
        {
            ExportToTSV(dataGridView2, "C:\\Users\\eriah\\source\\repos\\Data analysys\\Data analysys\\exports", "dataGridView2");
            ExportToTSV(dgvCounts, "C:\\Users\\eriah\\source\\repos\\Data analysys\\Data analysys\\exports","dgvCounts");
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }
    }
}
