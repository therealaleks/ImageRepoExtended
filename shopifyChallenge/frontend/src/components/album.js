import { Image } from "react-bootstrap";
import album from "../ressources/album.png";
import cross from "../ressources/cross.png";
import { useDrop, useDrag } from "react-dnd";
import { useAxios } from "../configs/requests";
function Album({ directory, refresh, setDir, handleDelete }) {
  const [{}, moveNode] = useAxios(
    {
      method: "PUT",
    },
    {
      manual: true,
    }
  );

  const handleMoveNode = (id, type) => {
    const formData = new FormData();
    formData.append("id", id);
    formData.append("parentId", directory.id);
    if (type == "media")
      moveNode({ data: formData, url: "/image/" + id + "/" }).then(() =>
        refresh()
      );
    else
      moveNode({ data: formData, url: "/directory/" + id + "/" }).then(() =>
        refresh()
      );
  };

  const [{ canDrop, isOver }, drop] = useDrop(() => ({
    accept: "BOX",
    drop: (item) => handleMoveNode(item.id, item.type),
    collect: (monitor) => ({
      isOver: monitor.isOver(),
      canDrop: monitor.canDrop(),
    }),
  }));

  const [{ isDragging }, drag] = useDrag(() => ({
    type: "BOX",
    item: { id: directory.id, type: "dir" },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  return (
    <div ref={drag} className="h-300 album">
      <Image
        ref={drop}
        onClick={() => setDir(directory)}
        src={album}
        className={"h-280 hover-zoom"}
      />
      {directory.name != ".." && (
        <Image
          src={cross}
          className="deleteBtn"
          onClick={() => handleDelete("/directory/" + directory.id + "/")}
        />
      )}
      {directory.name}
    </div>
  );
}

export default Album;
