export const getPexelsImageUrl = (id: number | null | undefined) => {//width: number, height: number
    if(!id) return undefined
    const width = 500;
    const height = 500;
    return `https://images.pexels.com/photos/${id}/pexels-photo-${id}.jpeg?auto=compress&cs=tinysrgb&w=${width}&h=${height}`
}
  