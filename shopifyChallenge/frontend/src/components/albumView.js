import ThumbNail from './Thumbnail';
import Video from './video';


function FlatView({images, videos}) {
    return (<div className='content'> 
        {images ? images.map((image)=><ThumbNail key={image.id} image={image}/>) : null} 
        {videos ? videos.map((video)=><Video key={video.id} video={video}/>) : null}
    </div>);
}

export default FlatView;