import { AgGridReact } from "ag-grid-react";
import { Table } from "antd";
import React, { useEffect, useState } from "react";
import { columnDef } from "../components/constants";

function AllStudentsList() {
  const [studentData, setStudentData] = useState([]);
  const columns = [
    {
      title: "Username",
      dataIndex: "username",
      key: "username",
    },
    {
      title: "Email",
      dataIndex: "email",
      key: "email",
    },
    {
      title: "Attendance days",
      dataIndex: "days",
      key: "days",
    },
    {
      title: "Delete",
      key: "key",
      dataIndex: "key",
      render: (text, record) => (
        <button onClick={() => deleteStudent(record.id)}>Delete</button>
      ),
    },
  ];
  const [columnDefs] = useState([
    {
      headerName: "Username",
      field: "username",
      type: "nonEditableColumn",
    },
    {
      headerName: "Email",
      field: "email",
      type: "nonEditableColumn",
    },

    {
      headerName: "Attendance Days",
      field: "days",
      type: "nonEditableColumn",
    },

    {
      field: "delete",
      cellRenderer: (p) => (
        <button onClick={() => deleteStudent(p.value)}>Delete</button>
      ),
    },
  ]);

  useEffect(() => {
    get_all_student_data();
  }, []);

  const get_all_student_data = () => {
    try {
      fetch("http://127.0.0.1:8000/student/get_all", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }).then((res) => {
        if (res.ok) {
          return res.json().then((val) => {
            if (val.code === 200) {
              setStudentData(val.data[0]);
            }
          });
        }
      });
    } catch (error) {
      console.log("Error : ", error);
    }
  };

  const deleteStudent = (id) => {
    try {
      console.log(id);
      fetch("http://127.0.0.1:8000/student/delete_student/" + id, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      }).then((res) => {
        if (res.ok) {
          res.json().then((val) => {
            if (val.code === 200) {
              alert(val.data);
              get_all_student_data();
            } else {
              alert(val.error);
            }
          });
        }
      });
    } catch (error) {
      console.log(error);
    }
  };
  console.log(studentData);

  return (
    <div>
      <h2>AllStudentsList</h2>
      <div>
        <Table
          dataSource={studentData}
          columns={columns}
          footer={false}
          pagination={false}
        />
      </div>
    </div>
  );
}

export default AllStudentsList;
