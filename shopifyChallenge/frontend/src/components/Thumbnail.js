import { Image } from "react-bootstrap";
import { useDrag } from "react-dnd";
import cross from "../ressources/cross.png";

function ThumbNail({ image, handleDelete }) {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: "BOX",
    item: { id: image.id, type: "media" },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));
  const content = image.content.content;

  return (
    <div>
      <a
        href={image.main_file}
        title={
          content.length > 0 ? content.toString() : "could not detect content"
        }
      >
        <Image
          ref={drag}
          src={image.main_file}
          className={"h-300 hover-zoom"}
          thumbnail
        />
      </a>
      <Image
        src={cross}
        className="deleteBtn"
        onClick={() => handleDelete("/image/" + image.id + "/")}
      />
    </div>
  );
}

export default ThumbNail;
