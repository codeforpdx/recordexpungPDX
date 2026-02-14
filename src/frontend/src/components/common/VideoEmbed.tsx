interface Props {
  src: string;
  title: string;
}

/**
 * Responsive 16:9 iframe wrapper for embedding YouTube videos.
 */
function VideoEmbed({ src, title }: Props) {
  return (
    <div className="aspect-ratio aspect-ratio--16x9 mb4 ba bw2 b--black-10">
      <iframe
        className="aspect-ratio--object"
        title={title}
        width={560}
        height={315}
        src={src}
        style={{ border: 0 }}
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      />
    </div>
  );
}

export default VideoEmbed;
