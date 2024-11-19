export const handleXScroll = (e) => {
  e.preventDefault();
  e.currentTarget.scrollLeft += e.deltaY;
};
