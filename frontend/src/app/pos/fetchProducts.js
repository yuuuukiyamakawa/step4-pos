export default async function fetchProducts(input_code) {
    const res = await fetch(process.env.API_ENDPOINT+`/products?code=${input_code}`, { cache: "no-cache" });
    // const res = await fetch(`http://127.0.0.1:8000/products?code=${input_code}`, { cache: "no-cache" })
    // console.log(res);

    if (!res.ok) {
      throw new Error('Failed to fetch products');
    }
    return res.json();
  }