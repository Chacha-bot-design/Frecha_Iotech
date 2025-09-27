useEffect(() => {
  const fetchData = async () => {
    try {
      setLoading(true);
      console.log('Starting API calls...');
      
      const [providersResponse, bundlesResponse, routersResponse] = await Promise.all([
        getProviders(),
        getBundles(),
        getRouters()
      ]);
      
      console.log('Raw API Responses:');
      console.log('Providers response:', providersResponse);
      console.log('Bundles response:', bundlesResponse);
      console.log('Routers response:', routersResponse);
      
      // Handle different response structures
      const getDataFromResponse = (response) => {
        // If response.data exists and is an array, use it
        if (response.data && Array.isArray(response.data)) {
          return response.data;
        }
        // If response itself is an array, use it directly
        if (Array.isArray(response)) {
          return response;
        }
        // Default to empty array
        return [];
      };
      
      const providersData = getDataFromResponse(providersResponse);
      const bundlesData = getDataFromResponse(bundlesResponse);
      const routersData = getDataFromResponse(routersResponse);
      
      console.log('Extracted Data:');
      console.log('Providers:', providersData);
      console.log('Bundles:', bundlesData);
      console.log('Routers:', routersData);
      
      setProviders(providersData);
      setBundles(bundlesData);
      setRouters(routersData);
      setLoading(false);
      
    } catch (err) {
      console.error('Error in fetchData:', err);
      setError('Failed to load data: ' + err.message);
      setLoading(false);
      setProviders([]);
      setBundles([]);
      setRouters([]);
    }
  };

  fetchData();
}, []);