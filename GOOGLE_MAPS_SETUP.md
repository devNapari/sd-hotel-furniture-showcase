# Google Maps Setup Guide

The contact page now includes an interactive Google Maps embed showing your business location.

## Current Setup

The map is currently showing the **Empire State Building** as a placeholder location. You need to update it with your actual business address.

## How to Customize the Map

### Option 1: Using Google Maps Embed (Current Method - No API Key Required)

This is the simplest method and doesn't require a Google Maps API key.

#### Step 1: Find Your Location

1. Go to [Google Maps](https://www.google.com/maps)
2. Search for your business address
3. Click on your location to select it

#### Step 2: Get the Embed Code

1. Click the **"Share"** button
2. Select the **"Embed a map"** tab
3. Choose your preferred size (we recommend "Large" or "Custom")
4. Click **"Copy HTML"**

#### Step 3: Extract the URL

From the copied HTML, extract just the URL from the `src` attribute. It will look like:
```
<iframe src="https://www.google.com/maps/embed?pb=!1m10!1m8!1m3!1d6181.741518466665!2d-0.8269203!3d9.3658472!3m2!1i1024!2i768!4f13.1!5e1!3m2!1sen!2sgh!4v1763059856666!5m2!1sen!2sgh" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d...
```

#### Step 4: Update the Contact Page

Edit `templates/contact.html` and replace the iframe src (around line 247):


<iframe
    src="https://www.google.com/maps/place/Tuutingli/@9.3669428,-0.8236374,17z/data=!4m14!1m7!3m6!1s0xfd43b43d6cdb0f9:0xe0743c14564ded6!2sTuutingli!8m2!3d9.3669375!4d-0.8210625!16s%2Fg%2F11stnzn6pw!3m5!1s0xfd43b43d6cdb0f9:0xe0743c14564ded6!8m2!3d9.3669375!4d-0.8210625!16s%2Fg%2F11stnzn6pw?entry=ttu&g_ep=EgoyMDI1MTExMC4wIKXMDSoASAFQAw%3D%3D"
    allowfullscreen=""
    loading="lazy"
    referrerpolicy="no-referrer-when-downgrade"
    title="SD Hotel Furniture Location">
</iframe>


#### Step 5: Update the Overlay Information

Update the map overlay card (around line 255) with your actual address:

```html
<div class="map-overlay d-none d-md-block">
    <h5 class="fw-bold"><i class="bi bi-geo-alt-fill text-danger me-2"></i>Visit Us</h5>
    <p class="mb-1"><strong>Your Business Name</strong></p>
    <p class="mb-1">Your Street Address</p>
    <p class="mb-1">City, State ZIP</p>
    <p class="mb-3">Country</p>
    <a href="https://www.google.com/maps/dir//YOUR_BUSINESS_NAME" target="_blank" class="btn btn-sm btn-primary">
        <i class="bi bi-map me-1"></i> Get Directions
    </a>
</div>
```

#### Step 6: Update Contact Information Section

Also update the address in the contact information section (around line 143):

```html
<p class="text-muted mb-0">Your Street Address<br>City, State ZIP<br>Country</p>
```

### Option 2: Using Coordinates (Alternative)

If you know your exact coordinates:

1. Get your latitude and longitude from Google Maps
2. Use this URL format:
```
https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d[ZOOM]!2d[LONGITUDE]!3d[LATITUDE]!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2sus
```

Replace:
- `[LATITUDE]` with your latitude
- `[LONGITUDE]` with your longitude
- `[ZOOM]` with zoom level (e.g., 3000 for street level)

### Option 3: Using Google Maps API (Advanced)

For more control and custom styling:

#### Step 1: Get API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Maps JavaScript API"
4. Create credentials (API Key)
5. Restrict the API key to your domain

#### Step 2: Add API Script

Add to the `<head>` section of `contact.html`:

```html
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap" async defer></script>
```

#### Step 3: Replace iframe with div

Replace the iframe with:

```html
<div id="map" style="width: 100%; height: 450px;"></div>
```

#### Step 4: Add JavaScript

Add this script before the closing `</body>` tag:

```javascript
function initMap() {
    // Your business location
    const location = { lat: YOUR_LATITUDE, lng: YOUR_LONGITUDE };
    
    // Create map
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: location,
        styles: [
            // Add custom styling here if desired
        ]
    });
    
    // Add marker
    const marker = new google.maps.Marker({
        position: location,
        map: map,
        title: 'SD Hotel Furniture'
    });
    
    // Add info window
    const infowindow = new google.maps.InfoWindow({
        content: `
            <div style="padding: 10px;">
                <h6>SD Hotel Furniture</h6>
                <p>123 Furniture Avenue<br>Design City, 12345</p>
                <a href="https://www.google.com/maps/dir//${location.lat},${location.lng}" target="_blank">Get Directions</a>
            </div>
        `
    });
    
    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
}
```

## Map Features

### Current Features

✅ **Interactive Map** - Users can zoom, pan, and explore
✅ **Responsive Design** - Works on all devices
✅ **Overlay Card** - Shows address with "Get Directions" button
✅ **Mobile Optimized** - Overlay hidden on small screens
✅ **Lazy Loading** - Map loads only when needed
✅ **Accessibility** - Proper title and attributes

### Customization Options

You can customize:

1. **Map Height** - Change `height: 450px` in the CSS
2. **Overlay Position** - Modify `top` and `left` values
3. **Overlay Style** - Update colors, padding, shadow
4. **Map Type** - Add `&maptype=satellite` to URL for satellite view
5. **Zoom Level** - Adjust in the embed URL

## Testing

After updating:

1. Visit `/contact` page
2. Verify the map shows your location
3. Test the "Get Directions" button
4. Check on mobile devices
5. Ensure overlay displays correctly

## Troubleshooting

### Map Not Loading

**Problem**: Gray box instead of map

**Solutions**:
- Check internet connection
- Verify the embed URL is correct
- Ensure no ad blockers are interfering
- Check browser console for errors

### Wrong Location

**Problem**: Map shows incorrect location

**Solutions**:
- Verify the embed URL
- Double-check coordinates if using Option 2
- Try generating a new embed code from Google Maps

### Overlay Not Showing

**Problem**: Address overlay not visible

**Solutions**:
- Check if viewing on mobile (overlay hidden on small screens)
- Verify CSS is loading correctly
- Check z-index values

### "Get Directions" Not Working

**Problem**: Button doesn't open directions

**Solutions**:
- Update the href with correct location name or coordinates
- Ensure target="_blank" is present
- Test the Google Maps URL directly

## Best Practices

### DO:
✅ Use your actual business address
✅ Test on multiple devices
✅ Keep the overlay information updated
✅ Use descriptive title attribute
✅ Enable lazy loading

### DON'T:
❌ Use fake or placeholder addresses
❌ Remove accessibility attributes
❌ Make the map too small (min 300px height)
❌ Forget to update all address references
❌ Use API key in public code (if using API method)

## Alternative Map Services

If you prefer not to use Google Maps:

### OpenStreetMap (Free)

```html
<iframe 
    width="100%" 
    height="450" 
    frameborder="0" 
    scrolling="no" 
    marginheight="0" 
    marginwidth="0" 
    src="https://www.openstreetmap.org/export/embed.html?bbox=WEST,SOUTH,EAST,NORTH&layer=mapnik&marker=LAT,LON">
</iframe>
```

### Mapbox (Customizable)

Requires API key but offers extensive customization options.

### Bing Maps

Microsoft's mapping service with embed options.

## Privacy Considerations

- Google Maps embed doesn't require cookies
- No personal data is collected
- Users can interact without tracking
- Consider adding to privacy policy

## Support

For issues:
1. Check Google Maps Help Center
2. Verify embed code is complete
3. Test in different browsers
4. Check browser console for errors

---

**Map is Ready!** Just update with your actual business location and you're all set.