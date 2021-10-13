import { useDrag } from "react-dnd";
import cross from "../ressources/cross.png";
import { Image } from "react-bootstrap";

function Video({ video, handleDelete }) {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: "BOX",
    item: { id: video.id, type: "media" },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));
  return (
    <div>
      <video
        ref={drag}
        src={video.main_file}
        className={"h-300 hover-zoom"}
        controls
      />
      <Image
        src={cross}
        className="deleteBtn"
        onClick={() => handleDelete("/video/" + video.id + "/")}
      />
    </div>
  );
}

export default Video;
