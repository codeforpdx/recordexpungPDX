interface Props {
  src: string;
  alt: string;
  caption: string;
  className?: string;
  imgClassName?: string;
  id?: string;
}

/**
 * Renders an image with a centered caption,
 * used for screenshots and diagrams in the Manual.
 */
function Figure({ src, alt, caption, className, imgClassName, id }: Props) {
  return (
    <figure className={`flex flex-column ma0 mb2 items-center ${className ?? ""}`}>
      <img src={src} alt={alt} className={`db ${imgClassName ?? ""}`} id={id} />
      <figcaption className="f6 gray tc mt2">{caption}</figcaption>
    </figure>
  );
}

export default Figure;
