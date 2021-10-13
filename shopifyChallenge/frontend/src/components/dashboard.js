import { useState, useRef, useEffect } from "react";
import { useAxios } from "../configs/requests";
import { Image, Form, Button, Dropdown } from "react-bootstrap";
import FlatView from "./flatView";
import uploadIcon from "../ressources/upload.png";
import refreshIcon from "../ressources/refresh.png";
import Select from "react-select";
import qs from "qs";

function Dashboard() {
  const [files, setFiles] = useState(null);
  const [filters, setFilters] = useState([]);
  const [orgView, setOrgView] = useState(false);
  const root = { id: "1", parentId: "1" };
  const [dir, setDir] = useState(root);
  const [parentDir, setParentDir] = useState(root);

  const mediaParams = qs.stringify({
    content: JSON.stringify(filters),
    ...(orgView && { parentId: dir.id }),
  });

  const [{ data: imageData }, getImages] = useAxios({
    method: "GET",
    url: "/image/?" + mediaParams,
  });

  const [{ data: videoData }, getVideos] = useAxios({
    method: "GET",
    url: "/video/?" + mediaParams,
  });

  const [{ data: dirData }, getDirs] = useAxios({
    method: "GET",
    url: "/directory/?" + mediaParams,
  });

  const [{ data: parentData }, getParentDir] = useAxios(
    {
      method: "GET",
      url: "/directory/" + dir.parentId + "/",
    },
    {
      manual: true,
    }
  );

  const [{}, upload] = useAxios(
    {
      method: "POST",
    },
    {
      manual: true,
    }
  );

  const [{}, postDir] = useAxios(
    {
      method: "POST",
      url: "/directory/",
    },
    {
      manual: true,
    }
  );

  const [{ data: imgSearchData }, imgSearch] = useAxios(
    {
      method: "POST",
      url: "/imageSearch/",
    },
    {
      manual: true,
    }
  );

  const filterOptions = [
    { value: "Person", label: "Person" },
    { value: "Man", label: "Man" },
    { value: "Woman", label: "Woman" },
    { value: "Plant", label: "Plant" },
    { value: "Tree", label: "Tree" },
    { value: "Building", label: "Building" },
    { value: "Food", label: "Food" },
    { value: "Animal", label: "Animal" },
    { value: "Dog", label: "Dog" },
    { value: "Cat", label: "Cat" },
    { value: "Fruit", label: "Fruit" },
    { value: "Car", label: "Car" },
  ];

  const get = () => {
    let params = {};

    if (orgView) params.parent = dir;

    getImages();
    getVideos();
    getDirs();
    getParentDir();
  };

  const handleCreateDir = (e) => {
    console.log(e);
    if (e.key == "Enter") {
      let dirName = e.target.value;
      let parentId = dir.id;

      const formData = new FormData();
      formData.append("name", dirName);
      formData.append("parentId", parentId);

      postDir({ data: formData }).then(() => get());
    }
  };

  const handleUpload = (search = false) => {
    if (files) {
      let posts = [];
      Object.values(files).forEach((file) => {
        const formData = new FormData();
        formData.append("title", file.name);
        formData.append("main_file", file, file.name);
        if (search) {
          posts.push(
            imgSearch({
              data: formData,
            })
          );
        } else {
          posts.push(
            upload({
              data: formData,
              url: file.type.split("/")[0] == "image" ? "/image/" : "/video/",
            })
          );
        }
      });

      Promise.all(posts).then(get);
    }
    setFiles(null);
  };

  const handleUploadChange = (e) => {
    if (e.target.files?.length > 0) setFiles([...e.target.files]);
    e.target.value = null;
  };

  useEffect(() => {
    get();
  }, [orgView, dir]);

  useEffect(() => {
    setParentDir(parentData);
  }, [parentData]);

  return (
    <div className="App">
      <h1> Simple Image Repo </h1>
      <div className="menu">
        <Form.Control
          id="upload-photo"
          onChange={handleUploadChange}
          type="file"
          className="uploadbtn"
          hidden
        />
        {imgSearchData ? (
          <Image
            src={refreshIcon}
            className="uploadButton"
            onClick={() => window.location.reload()}
          />
        ) : (
          <>
            <label htmlFor="upload-photo">
              <Image src={uploadIcon} className="uploadButton" />
            </label>
            {files ? files[0]?.name : "No file selected"}
          </>
        )}
        <div className="action">
          <Button onClick={() => handleUpload(false)} variant="secondary">
            upload
          </Button>
          <Button onClick={() => handleUpload(true)} variant="secondary">
            search
          </Button>
        </div>
        <Select
          options={filterOptions}
          className="filterSelector"
          placeholder="Select content filter categories"
          isMulti
          onChange={(options) =>
            setFilters(options.map((option) => option.value))
          }
        />
        <Form.Check
          type="switch"
          id="custom-switch"
          label="Organizational view"
          onClick={() => setOrgView(!orgView)}
        />
      </div>
      {orgView && (
        <center>
          <Form.Group
            className="mb-3 w-25"
            controlId="exampleForm.ControlInput1"
          >
            <Form.Label>New directory</Form.Label>
            <Form.Control
              placeholder="Directory name"
              onKeyPress={(e) => handleCreateDir(e)}
            />
          </Form.Group>
        </center>
      )}
      <div>
        <FlatView
          refresh={() => get()}
          images={imgSearchData ? imgSearchData : imageData}
          videos={imgSearchData ? [] : videoData}
          dirs={
            imgSearchData
              ? []
              : orgView && [
                  ...(dir.id != "1" ? [{ ...parentDir, name: ".." }] : []),
                  ...dirData.filter((dir) => dir.id != "1"),
                ]
          }
          setDir={(dirId) => setDir(dirId)}
        />
      </div>
    </div>
  );
}

export default Dashboard;
