import ThumbNail from "./Thumbnail";
import Video from "./video";
import Album from "./album";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { Form } from "react-bootstrap";
import { useAxios } from "../configs/requests";

function FlatView({ refresh, images, videos, dirs, setDir }) {
  const [{}, deleteNode] = useAxios(
    {
      method: "DELETE",
    },
    {
      manual: true,
    }
  );

  const handleDeleteNode = (url) => {
    deleteNode({ url: url }).then(() => refresh());
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="content">
        {dirs
          ? dirs.map((dir) => (
              <Album
                key={dir.id}
                directory={dir}
                refresh={refresh}
                setDir={setDir}
                handleDelete={handleDeleteNode}
              />
            ))
          : null}
        {images
          ? images.map((image) => (
              <ThumbNail
                key={image.id}
                image={image}
                handleDelete={handleDeleteNode}
              />
            ))
          : null}
        {videos
          ? videos.map((video) => (
              <Video
                key={video.id}
                video={video}
                handleDelete={handleDeleteNode}
              />
            ))
          : null}
      </div>
    </DndProvider>
  );
}

export default FlatView;
